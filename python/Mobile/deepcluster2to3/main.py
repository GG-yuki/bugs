# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import argparse
import torch.backends.cudnn as cudnn
import torch.nn.parallel
import torch.optim
import torch.utils.data
from sklearn.metrics.cluster import normalized_mutual_info_score
import clustering
from support import *
from util import Logger, UnifLabelSampler
from mobilenetv1_sobel import *
from torchvision import datasets
from vgg16 import *
import os


def parse_args():
    parser = argparse.ArgumentParser(description='PyTorch Implementation of DeepCluster')
    # parser.add_argument('--sobel', action='store_true', help='Sobel filtering')
    parser.add_argument('--clustering', type=str, choices=['Kmeans', 'PIC'],
                        default='Kmeans', help='clustering algorithm (default: Kmeans)')
    parser.add_argument('--lr', default=0.05, type=float,
                        help='learning rate (default: 0.05)')
    parser.add_argument('--wd', default=-5, type=float,
                        help='weight decay pow (default: -5)')
    parser.add_argument('--reassign', type=float, default=1.,
                        help="""how many epochs of training between two consecutive
                        reassignments of clusters (default: 1)""")
    parser.add_argument('--workers', default=4, type=int,
                        help='number of data loading workers (default: 4)')
    parser.add_argument('--epochs', type=int, default=200,
                        help='number of total epochs to run (default: 200)')
    parser.add_argument('--start_epoch', default=0, type=int,
                        help='manual epoch number (useful on restarts) (default: 0)')
    parser.add_argument('--batch', default=32, type=int,
                        help='mini-batch size (default: 256)')
    parser.add_argument('--momentum', default=0.9, type=float, help='momentum (default: 0.9)')
    parser.add_argument('--nmb_cluster', '--k', type=int, default=2,
                        help='number of cluster for k-means (default: 2)')
    return parser.parse_args()


def main(args):
    # fix random seeds
    seed(31)

    # CNN
    model = MobileNetV1(num_classes=100, sobel=True)
    fd = int(model.top_layer.weight.size()[1])
    model.top_layer = None
    model.features = torch.nn.DataParallel(model.features)
    model.cuda()
    cudnn.benchmark = True

    # create optimizer
    optimizer = torch.optim.SGD(
        [x for x in model.parameters() if x.requires_grad],
        lr=args.lr,
        momentum=args.momentum,
        weight_decay=10 ** args.wd,
    )

    # define loss function
    criterion = nn.CrossEntropyLoss().cuda()

    # creating cluster assignments log
    cluster_log = Logger(os.path.join('./image_list_log/', 'clusters'))
    end = time.time()
    # load the data
    dataset = datasets.ImageFolder(root=r'./dataset/train',
                                   transform=transform())
    dataloader = torch.utils.data.DataLoader(dataset,
                                             batch_size=args.batch,
                                             num_workers=args.workers,
                                             pin_memory=True)

    # clustering algorithm to use
    deepcluster = clustering.__dict__[args.clustering](args.nmb_cluster)
    print('start train')

    # training convnet with DeepCluster
    for epoch in range(args.start_epoch, args.epochs):
        print(epoch)
        # remove head
        model.top_layer = None
        model.classifier = nn.Sequential(*list(model.classifier.children())[:-1])

        # get the features for the whole dataset
        features = compute_features(dataloader, model, len(dataset), args.batch)

        # cluster the feature
        clustering_loss = deepcluster.cluster(features)

        # assign pseudo-labels
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
        mlp = list(model.classifier.children())
        mlp.append(nn.ReLU(inplace=True).cuda())
        model.classifier = nn.Sequential(*mlp)
        model.top_layer = nn.Linear(fd, len(deepcluster.images_lists))
        model.top_layer.weight.data.normal_(0, 0.01)
        model.top_layer.bias.data.zero_()
        model.top_layer.cuda()

        # train network with clusters as pseudo-labels
        end = time.time()
        loss = train(train_dataloader, model, criterion, optimizer, epoch, args.lr, args.wd)

        # print log
        # print('###### Epoch [{0}] ###### \n'
        #       'Time: {1:.3f} s\n'
        #       'Clustering loss: {2:.3f} \n'
        #       'ConvNet loss: {3:.3f}'
        #       .format(epoch, time.time() - end, clustering_loss, loss))
        try:
            nmi = normalized_mutual_info_score(
                clustering.arrange_clustering(deepcluster.images_lists),
                clustering.arrange_clustering(cluster_log.data[-1])
            )
            print('NMI against previous assignment: {0:.3f}'.format(nmi))
            f = open('result.txt', "a")
            f.write('NMI against previous assignment: {0:.3f}'.format(nmi))
            f.close()
            # print(loss)
        except IndexError:
            pass
        print('####################### \n')
        # save cluster assignments
        cluster_log.log(deepcluster.images_lists)


if __name__ == '__main__':
    args = parse_args()
    main(args)
