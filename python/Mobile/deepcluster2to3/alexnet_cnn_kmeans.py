# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import argparse
import os
import time

import numpy as np
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torchvision.transforms as transforms
import torchvision.datasets as datasets

from util import AverageMeter, learning_rate_decay, load_model, Logger

parser = argparse.ArgumentParser(description="""Train linear classifier on top
                                 of frozen convolutional layers of an AlexNet.""")

parser.add_argument('--data', type=str, help='path to dataset')
parser.add_argument('--model', type=str, help='path to model')
parser.add_argument('--conv', type=int, choices=[1, 2, 3, 4, 5],
                    help='on top of which convolutional layer train logistic regression')
parser.add_argument('--tencrops', action='store_true',
                    help='validation accuracy averaged over 10 crops')
parser.add_argument('--exp', type=str, default='', help='exp folder')
parser.add_argument('--workers', default=4, type=int,
                    help='number of data loading workers (default: 4)')
parser.add_argument('--epochs', type=int, default=90, help='number of total epochs to run (default: 90)')
parser.add_argument('--batch_size', default=256, type=int,
                    help='mini-batch size (default: 256)')
parser.add_argument('--lr', default=0.01, type=float, help='learning rate')
parser.add_argument('--momentum', default=0.9, type=float, help='momentum (default: 0.9)')
parser.add_argument('--weight_decay', '--wd', default=-4, type=float,
                    help='weight decay pow (default: -4)')
parser.add_argument('--seed', type=int, default=31, help='random seed')
parser.add_argument('--verbose', action='store_true', help='chatty')


def main():
    global args
    args = parser.parse_args()

    # fix random seeds
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    np.random.seed(args.seed)

    best_prec1 = 0

    # load model
    model = load_model()
    model.cuda()
    cudnn.benchmark = True

    # freeze the features layers
    for param in model.features.parameters():
        param.requires_grad = False

    # define loss function (criterion) and optimizer
    criterion = nn.CrossEntropyLoss().cuda()

    # data loading code

    normalize = transforms.Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.24703223, 0.24348512, 0.26158784])

    transformations_val = [transforms.Resize(256),
                           transforms.CenterCrop(224),
                           transforms.ToTensor(),
                           normalize]

    transformations_train = [transforms.Resize(256),
                             transforms.CenterCrop(256),
                             transforms.RandomCrop(224),
                             transforms.RandomHorizontalFlip(),
                             transforms.ToTensor(),
                             normalize]
    train_dataset = datasets.ImageFolder(
        r'./dataset/train',
        transform=transforms.Compose(transformations_train)
    )

    val_dataset = datasets.ImageFolder(
        r'./dataset/test',
        transform=transforms.Compose(transformations_val)
    )
    train_loader = torch.utils.data.DataLoader(train_dataset,
                                               batch_size=args.batch_size,
                                               shuffle=True,
                                               num_workers=args.workers,
                                               pin_memory=True)
    val_loader = torch.utils.data.DataLoader(val_dataset,
                                             batch_size=int(args.batch_size / 2),
                                             shuffle=False,
                                             num_workers=args.workers)

    # logistic regression
    reglog = RegLog(5, len(train_dataset.classes)).cuda()
    print(len(train_dataset.classes))
    optimizer = torch.optim.SGD(
        filter(lambda x: x.requires_grad, reglog.parameters()),
        args.lr,
        momentum=args.momentum,
        weight_decay=10 ** args.weight_decay
    )

    for epoch in range(args.epochs):
        end = time.time()

        # train for one epoch
        train(train_loader, model, reglog, criterion, optimizer, epoch)

        # evaluate on validation set
        prec1, prec5, loss = validate(val_loader, model, reglog, criterion)

        # remember best prec@1 and save checkpoint
        is_best = prec1 > best_prec1
        best_prec1 = max(prec1, best_prec1)


class RegLog(nn.Module):
    """Creates logistic regression on top of frozen features"""

    def __init__(self, conv, num_labels):
        super(RegLog, self).__init__()
        self.conv = conv
        if conv == 1:
            self.av_pool = nn.AvgPool2d(6, stride=6, padding=3)
            s = 9600
        elif conv == 2:
            self.av_pool = nn.AvgPool2d(4, stride=4, padding=0)
            s = 9216
        elif conv == 3:
            self.av_pool = nn.AvgPool2d(3, stride=3, padding=1)
            s = 9600
        elif conv == 4:
            self.av_pool = nn.AvgPool2d(3, stride=3, padding=1)
            s = 9600
        elif conv == 5:
            self.av_pool = nn.AvgPool2d(2, stride=2, padding=0)
            s = 9216
        self.linear = nn.Linear(s, num_labels)

    def forward(self, x):
        x = self.av_pool(x)
        x = x.view(x.size(0), x.size(1) * x.size(2) * x.size(3))
        return self.linear(x)


def forward(x, model, conv):
    if hasattr(model, 'sobel') and model.sobel is not None:
        x = model.sobel(x)
    count = 1
    for m in model.features.modules():
        if not isinstance(m, nn.Sequential):
            x = m(x)
        if isinstance(m, nn.ReLU):
            if count == conv:
                return x
            count = count + 1
    return x


def accuracy(output, target, topk=(1,)):
    """Computes the precision@k for the specified values of k"""
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res


def train(train_loader, model, reglog, criterion, optimizer, epoch):
    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()
    top5 = AverageMeter()

    # freeze also batch norm layers
    model.eval()

    end = time.time()
    prec1 = 0
    train_total = 0
    for i, (input, target) in enumerate(train_loader):

        # measure data loading time
        data_time.update(time.time() - end)

        # adjust learning rate
        learning_rate_decay(optimizer, len(train_loader) * epoch + i, args.lr)

        target = target.cuda()
        input_var = torch.autograd.Variable(input.cuda())
        target_var = torch.autograd.Variable(target)
        # compute output

        output = forward(input_var, model, reglog.conv)
        output = reglog(output)
        loss = criterion(output, target_var)
        # measure accuracy and record loss
        _, train_predicted = torch.max(output.data, 1)
        prec1 += (train_predicted == target_var.data).sum()
        train_total += target.size(0)
        # losses.update(loss.data[0], input.size(0))

        # compute gradient and do SGD step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

    print(prec1/train_total)


def validate(val_loader, model, reglog, criterion):
    batch_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()
    top5 = AverageMeter()

    # switch to evaluate mode
    model.eval()
    softmax = nn.Softmax(dim=1).cuda()
    end = time.time()
    prec1 = 0
    train_total = 0
    for i, (input_tensor, target) in enumerate(val_loader):
        if args.tencrops:
            bs, ncrops, c, h, w = input_tensor.size()
            input_tensor = input_tensor.view(-1, c, h, w)
        target = target.cuda()
        input_var = torch.autograd.Variable(input_tensor.cuda())
        target_var = torch.autograd.Variable(target)

        output = reglog(forward(input_var, model, reglog.conv))

        if args.tencrops:
            output_central = output.view(bs, ncrops, -1)[:, ncrops / 2 - 1, :]
            output = softmax(output)
            output = torch.squeeze(output.view(bs, ncrops, -1).mean(1))
        else:
            output_central = output

        _, train_predicted = torch.max(output.data, 1)
        prec1 += (train_predicted == target_var.data).sum()
        loss = criterion(output_central, target_var)
        train_total += target.size(0)

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

    top1 = 0
    top5 = 0
    losses = 0
    print(prec1/train_total)

    return top1, top5, losses


if __name__ == '__main__':
    main()
