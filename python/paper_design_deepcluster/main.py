# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import argparse
import os
import pickle
import time
import numpy as np
from sklearn.metrics.cluster import normalized_mutual_info_score
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torchvision.datasets as datasets
from support import *
import clustering
from vgg16 import vgg16
from util import AverageMeter, Logger, UnifLabelSampler


def parse_args():
    parser = argparse.ArgumentParser(description='PyTorch Implementation of DeepCluster')
    parser.add_argument('--arch', '-a', type=str, metavar='ARCH',
                        choices=['alexnet', 'vgg16'], default='alexnet',
                        help='CNN architecture (default: alexnet)')
    parser.add_argument('--sobel', action='store_true', help='Sobel filtering')
    parser.add_argument('--clustering', type=str, choices=['Kmeans', 'PIC'],
                        default='Kmeans', help='clustering algorithm (default: Kmeans)')
    parser.add_argument('--nmb_cluster', '--k', type=int, default=2,
                        help='number of cluster for k-means (default: 2)')
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
                        help='mini-batch size (default: 32)')
    parser.add_argument('--momentum', default=0.9, type=float, help='momentum (default: 0.9)')
    parser.add_argument('--resume', default=r'/home/jijl/My_project/paper_design_deepcluster/check', type=str, metavar='PATH',
                        help='path to checkpoint (default: None)')
    parser.add_argument('--checkpoints', type=int, default=25000,
                        help='how many iterations between two checkpoints (default: 25000)')
    parser.add_argument('--exp', type=str, default=r'/home/jijl/My_project/paper_design_deepcluster/check', help='path to exp folder')
    return parser.parse_args()


def main(args):
    # fix random seeds
    torch.manual_seed(31)
    torch.cuda.manual_seed_all(31)
    np.random.seed(31)

    # CNN
    model = vgg16(sobel=True) #?
    fd = int(model.top_layer.weight.size()[1])
    model.top_layer = None
    model.features = torch.nn.DataParallel(model.features)
    model.cuda()
    cudnn.benchmark = True

    # create optimizer
    optimizer = torch.optim.SGD(
        filter(lambda x: x.requires_grad, model.parameters()),
        lr=0.05,
        momentum=0.9,
        weight_decay=10**(-5),
    )

    # define loss function
    criterion = nn.CrossEntropyLoss().cuda()

    # creating cluster assignments log
    cluster_log = Logger(r'exp.txt')

    # load the data
    end = time.time()
    data_transform = datatransform()
    dataset = datasets.ImageFolder(root=r'/home/jijl/My_project/paper_design_deepcluster/sdsds', transform=data_transform)
    print('Load dataset: {0:.2f} s'.format(time.time() - end))

    dataloader = torch.utils.data.DataLoader(dataset,
                                             batch_size=args.batch,
                                             num_workers=args.workers,
                                             pin_memory=True)

    # clustering algorithm to use
    deepcluster = clustering.__dict__[args.clustering](args.nmb_cluster)

    # training convnet with DeepCluster
    for epoch in range(args.start_epoch, args.epochs):

        end = time.time()
        print(epoch)
        # remove head
        model.top_layer = None
        model.classifier = nn.Sequential(*list(model.classifier.children())[:-1])

        # get the features for the whole dataset
        features = compute_features(dataloader, model, len(dataset))

        # cluster the features
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
        loss = train(train_dataloader, model, criterion, optimizer, epoch)

        print('###### Epoch [{0}] ###### \n'
              'Time: {1:.3f} s\n'
              'Clustering loss: {2:.3f} \n'
              'ConvNet loss: {3:.3f}'
              .format(epoch, time.time() - end, clustering_loss, loss))
        try:
            nmi = normalized_mutual_info_score(
                clustering.arrange_clustering(deepcluster.images_lists),
                clustering.arrange_clustering(cluster_log.data[-1])
            )
            print('NMI against previous assignment: {0:.3f}'.format(nmi))
        except IndexError:
            pass
        print('####################### \n')
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
        lr=0.05,
        weight_decay=10**(-5),
    )

    end = time.time()
    for i, (input_tensor, target) in enumerate(loader):
        data_time.update(time.time() - end)

        target = target.cuda()
        input_var = torch.autograd.Variable(input_tensor.cuda())
        target_var = torch.autograd.Variable(target)

        output = model(input_var)
        loss = crit(output, target_var)

        # record loss
        losses.update(loss.item(), input_tensor.size(0))


        # compute gradient and do SGD stepa
        opt.zero_grad()
        optimizer_tl.zero_grad()
        loss.backward()
        opt.step()
        optimizer_tl.step()

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

    return losses.avg

def compute_features(dataloader, model, N):
    batch_time = AverageMeter()
    end = time.time()
    model.eval()
    # discard the label information in the dataloader
    for i, (input_tensor, _) in enumerate(dataloader):
        with torch.no_grad():
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

    return features


if __name__ == '__main__':
    args = parse_args()
    main(args)