# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
import argparse
from sklearn.metrics.cluster import normalized_mutual_info_score
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torchvision.datasets as datasets

import clustering
# from mobilenetv1_sobel import *
# from mobilenetv2_another_sobel import *
# from mobilenetv3_another_sobel import *
from mobilenetv3_with_sobel import *
from util import *
import os
from support import *
from alexnet import alexnet


# os.environ['CUDA_VISIBLE_DEVICES'] = '2'


def parse_args():
    parser = argparse.ArgumentParser(description='PyTorch Implementation of DeepCluster')
    parser.add_argument('--arch', '-a', type=str, metavar='ARCH',
                        choices=['alexnet', 'vgg16'], default='alexnet',
                        help='CNN architecture (default: alexnet)')
    parser.add_argument('--sobel', action='store_true', help='Sobel filtering')
    parser.add_argument('--clustering', type=str, choices=['Kmeans', 'PIC'],
                        default='Kmeans', help='clustering algorithm (default: Kmeans)')
    parser.add_argument('--nmb_cluster', '--k', type=int, default=100,
                        help='number of cluster for k-means (default: 10000)')
    parser.add_argument('--lr', default=0.005, type=float,
                        help='learning rate (default: 0.05)')
    parser.add_argument('--wd', default=-5, type=float,
                        help='weight decay pow (default: -5)')
    parser.add_argument('--reassign', type=float, default=1.,
                        help="""how many epochs of training between two consecutive
                        reassignments of clusters (default: 1)""")
    parser.add_argument('--workers', default=0, type=int,
                        help='number of data loading workers (default: 4)')
    parser.add_argument('--epochs', type=int, default=200,
                        help='number of total epochs to run (default: 200)')
    parser.add_argument('--start_epoch', default=0, type=int,
                        help='manual epoch number (useful on restarts) (default: 0)')
    parser.add_argument('--batch', default=1, type=int,
                        help='mini-batch size (default: 256)')
    parser.add_argument('--momentum', default=0.9, type=float, help='momentum (default: 0.9)')
    parser.add_argument('--resume', default='', type=str, metavar='PATH',
                        help='path to checkpoint (default: None)')
    parser.add_argument('--seed', type=int, default=31, help='random seed (default: 31)')
    parser.add_argument('--exp', type=str, default='', help='path to exp folder')
    return parser.parse_args()


def main(args):
    # fix random seeds
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    np.random.seed(args.seed)

    # CNN
    # if args.verbose:
    #     print('Architecture: {}'.format(args.arch))
    # model = load_net('149')
    # model = mobilenet_v3_large(pretrained=False, sobel=True, num_classes=100)
    model = MobileNetV3_Small(num_classes=100, sobel=True)
    # model = alexnet(sobel=True)
    # fd = 1000
    # print(fd)
    fd = int(model.top_layer.weight.size()[1])
    model.top_layer = None
    model.features = torch.nn.DataParallel(model.features)
    model.cuda()
    cudnn.benchmark = True

    # create optimizer
    optimizer = torch.optim.SGD(
        filter(lambda x: x.requires_grad, model.parameters()),
        lr=args.lr,
        momentum=args.momentum,
        weight_decay=10 ** args.wd,
    )

    # define loss function
    criterion = nn.CrossEntropyLoss().cuda()

    # creating cluster assignments log
    cluster_log = Logger(os.path.join('./image_list_log/', 'clusters'))

    normalize = transforms.Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.24703223, 0.24348512, 0.26158784])

    # preprocessing of data
    tra = [transforms.Resize(256),
           transforms.CenterCrop(224),
           transforms.ToTensor(),
           normalize
           ]

    # load the data
    end = time.time()
    dataset = datasets.ImageFolder(r'./dataset/train', transform=transforms.Compose(tra))

    dataloader = torch.utils.data.DataLoader(dataset,
                                             batch_size=args.batch,
                                             num_workers=args.workers,
                                             pin_memory=True)

    # clustering algorithm to use
    deepcluster = clustering.__dict__[args.clustering](args.nmb_cluster)

    # training convnet with DeepCluster
    for epoch in range(args.start_epoch, args.epochs):
        end = time.time()

        # remove head
        model.top_layer = None
        model.classifier = nn.Sequential(*list(model.classifier.children())[:-1])
        # print(model.classifier)
        # get the features for the whole dataset
        features = compute_features(dataloader, model, len(dataset))

        # cluster the features
        # if args.verbose:
        #     print('Cluster the features')
        clustering_loss = deepcluster.cluster(features)

        # assign pseudo-labels
        # if args.verbose:
        #     print('Assign pseudo labels')
        train_dataset = clustering.cluster_assign(deepcluster.images_lists,
                                                  dataset.imgs)

        # uniformly sample per target
        sampler = UnifLabelSampler(int(args.reassign * len(train_dataset)),
                                   deepcluster.images_lists)

        train_dataloader = torch.utils.data.DataLoader(
            train_dataset,
            batch_size=args.batch,
            num_workers=args.workers,
            sampler=sampler,
            pin_memory=True,
        )

        # set last fully connected layer
        # mlp = list()
        # mlp.append(nn.Linear(in_features=1024, out_features=1000, bias=True).cuda())
        mlp = list(model.classifier.children())
        mlp.append(nn.ReLU(inplace=True).cuda())
        # print(mlp)
        model.classifier = nn.Sequential(*mlp)
        model.top_layer = nn.Linear(fd, len(deepcluster.images_lists))
        # print(len(deepcluster.images_lists))
        model.top_layer.weight.data.normal_(0, 0.01)
        model.top_layer.bias.data.zero_()
        model.top_layer.cuda()

        # train network with clusters as pseudo-labels
        end = time.time()
        loss = train(train_dataloader, model, criterion, optimizer, epoch)

        try:
            nmi = normalized_mutual_info_score(
                clustering.arrange_clustering(deepcluster.images_lists),
                clustering.arrange_clustering(cluster_log.data[-1])
            )
            print('NMI against previous assignment: {0:.3f}'.format(nmi))
            f = open('NMI_result.txt', "a")
            f.write('NMI against previous assignment: {0:.3f}'.format(nmi))
            f.write("  epoch: %d \n" % epoch)
            f.close()
        except IndexError:
            pass
        print('####################### \n')
        # save running checkpoint
        torch.save({'epoch': epoch + 1,
                    'arch': args.arch,
                    'state_dict': model.state_dict(),
                    'optimizer': optimizer.state_dict()},
                   r'./exp/checkpoint_mobilenetv3_small.pth.tar')

        # save cluster assignments
        cluster_log.log(deepcluster.images_lists)


def train(loader, model, crit, opt, epoch):
    """Training of the CNN.
        Args:
            loader (torch.utils.data.DataLoader): Data loader
            model (nn.Module): CNN
            crit (torch.nn): loss
            opt (torch.optim.SGD): optimizer for every parameters with True
                                   requires_grad in model except top layer
            epoch (int)
    """
    batch_time = AverageMeter()
    losses = AverageMeter()
    data_time = AverageMeter()
    forward_time = AverageMeter()
    backward_time = AverageMeter()

    # switch to train mode
    model.train()

    # create an optimizer for the last fc layer
    optimizer_tl = torch.optim.SGD(
        model.top_layer.parameters(),
        lr=args.lr,
        weight_decay=10 ** args.wd,
    )

    end = time.time()
    print(epoch)
    for i, (input_tensor, target) in enumerate(loader):
        data_time.update(time.time() - end)

        # save checkpoint
        n = len(loader) * epoch + i
        input_var = torch.autograd.Variable(input_tensor.cuda())
        target_var = torch.autograd.Variable(target.cuda())

        output = model(input_var)
        loss = crit(output, target_var)

        # record loss
        # losses.update(loss.data[0], input_tensor.size(0))

        # compute gradient and do SGD step
        opt.zero_grad()
        optimizer_tl.zero_grad()
        loss.backward()
        opt.step()
        optimizer_tl.step()

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()
        # sava_params(epoch, model, opt, r'mobilenetv1_30')

        if (epoch + 1) / 10 == 1:
            save_net(model, epoch)
            sava_params(epoch, model, opt, r'mobilenetv3_small_10')
        if (epoch + 1) / 30 == 1:
            save_net(model, epoch)
            sava_params(epoch, model, opt, r'mobilenetv3_small_30')
        if (epoch + 1) / 60 == 1:
            save_net(model, epoch)
            sava_params(epoch, model, opt, r'mobilenetv3_small_60')
        if (epoch + 1) / 90 == 1:
            save_net(model, epoch)
            sava_params(epoch, model, opt, r'mobilenetv3_small_90')
        if (epoch + 1) / 100 == 1:
            save_net(model, epoch)
            sava_params(epoch, model, opt, r'mobilenetv3_small_100')
    return losses.avg


def compute_features(dataloader, model, N):
    batch_time = AverageMeter()
    end = time.time()
    model.eval()
    # discard the label information in the dataloader
    for i, (input_tensor, _) in enumerate(dataloader):
        input_var = torch.autograd.Variable(input_tensor.cuda())
        aux = model(input_var).data.cpu().numpy()

        if i == 0:
            features = np.zeros((N, aux.shape[1]), dtype='float32')

        aux = aux.astype('float32')
        if i < len(dataloader) - 1:
            features[i * args.batch: (i + 1) * args.batch] = aux
        else:
            # special treatment for final batch
            features[i * args.batch:] = aux

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        # if i % 200 == 0:
        #     print('{0} / {1}\t'
        #           'Time: {batch_time.val:.3f} ({batch_time.avg:.3f})'
        #           .format(i, len(dataloader), batch_time=batch_time))
    return features


if __name__ == '__main__':
    args = parse_args()
    main(args)
