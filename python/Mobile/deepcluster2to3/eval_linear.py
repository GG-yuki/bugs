# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import argparse
import numpy as np
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torchvision.datasets as datasets
import torchvision.transforms as transforms

# from mobilenetv1_sobel import *
from mobilenetv1_no_sobel import *
from util import learning_rate_decay, load_model, write_result

parser = argparse.ArgumentParser(description="""Train linear classifier on top
                                 of frozen convolutional layers of an AlexNet.""")

parser.add_argument('--data', type=str, help='path to dataset')
parser.add_argument('--model', type=str, help='path to model')
parser.add_argument('--exp', type=str, default='', help='exp folder')
parser.add_argument('--workers', default=0, type=int,
                    help='number of data loading workers (default: 4)')
parser.add_argument('--epochs', type=int, default=90, help='number of total epochs to run (default: 90)')
parser.add_argument('--batch_size', default=32, type=int,
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

    # load model
    # model = nn.DataParallel(Resnet18())
    # model.load_state_dict(torch.load(path))
    # model = model.module
    # cudnn.benchmark = True

    # net = MobileNetV1(num_classes=100,sobel=True)
    # model = load_model()
    # model.top_layer = nn.Linear(1000, 100)
    # print(model)
    # model.cuda()
    # cudnn.benchmark = True
    #
    # freeze the features layers

    model = load_model()
    model.top_layer = None
    model.classifier = nn.Linear(1024, 10)
    model.cuda()
    cudnn.benchmark = True

    for param in model.features.parameters():
        param.requires_grad = False

    # define loss function (criterion) and optimizer
    criterion = nn.CrossEntropyLoss().cuda()

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

    train_dataset = datasets.ImageFolder(r'./dataset/train',
                                         transform=transforms.Compose(transformations_train))

    val_dataset = datasets.ImageFolder(r'./dataset/test', transform=transforms.Compose(transformations_val))

    train_loader = torch.utils.data.DataLoader(train_dataset,
                                               batch_size=args.batch_size,
                                               shuffle=True,
                                               num_workers=args.workers,
                                               pin_memory=True)
    val_loader = torch.utils.data.DataLoader(val_dataset,
                                             batch_size=int(args.batch_size / 2),
                                             shuffle=False,
                                             num_workers=args.workers)

    optimizer = torch.optim.SGD(
        model.parameters(),
        args.lr,
        momentum=args.momentum,
        weight_decay=10 ** args.weight_decay
    )

    model_name = format(model.__class__.__name__)
    with open('./experiment_record(first)/' + model_name + '/result.txt', "w") as f:
        f.write("开始实验\n")  # 自带文件关闭功能，不需要再写f.close()

    # reglog = RegLog(args.conv, len(train_dataset.classes)).cuda()
    # optimizer = torch.optim.SGD(
    #     filter(lambda x: x.requires_grad, reglog.parameters()),
    #     args.lr,
    #     momentum=args.momentum,
    #     weight_decay=10**args.weight_decay
    # )

    # create logs
    # exp_log = os.path.join(args.exp, 'log')
    # if not os.path.isdir(exp_log):
    #     os.makedirs(exp_log)
    result = train(args.epochs, train_loader, model, criterion, optimizer, val_loader)
    write_result(format(model.__class__.__name__), args.epochs, args.batch_size, args.num_workers, args.lr, result, args.weight_decay)


def train(epochs, train_loader, model, criterion, optimizer, val_loader):
    model_name = format(model.__class__.__name__)
    max_acc = 0
    # freeze also batch norm layers
    model.eval()

    for epoch in range(epochs):
        train_correct = 0
        train_total = 0
        running_loss = 0.0
        for i, (train_input, target) in enumerate(train_loader):
            # adjust learning rate
            learning_rate_decay(optimizer, len(train_loader) * epoch + i, args.lr)

            input_var = torch.autograd.Variable(train_input.cuda())
            target_var = torch.autograd.Variable(target.cuda())
            # compute output
            output = model(input_var)
            # output = model(output)
            loss = criterion(output, target_var)
            # measure accuracy and record loss
            _, train_predicted = torch.max(output.data, 1)
            train_correct += (train_predicted == target_var.data).sum()
            running_loss += loss.item()
            train_total += target.size(0)

            # compute gradient and do SGD step
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        print('train %d epoch loss: %.3f  acc: %.3f' % (
            epoch + 1, running_loss / train_total, 100 * train_correct / train_total))
        f = open('./experiment_record(first)/' + model_name + '/result.txt', "a")
        f.write('train %d epoch loss: %.3f  acc: %.3f\n' % (
            epoch + 1, running_loss / train_total, 100 * train_correct / train_total))
        f.close()
        # print('Epoch: [{0}][{1}/{2}]\t'
        #       'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
        #       'Data {data_time.val:.3f} ({data_time.avg:.3f})\t'
        #       'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
        #       'Prec_acc {acc:.3f}\t'
        #       .format(epoch, i, len(train_loader), batch_time=batch_time,
        #               data_time=data_time, loss=losses, acc = 100 * train_correct / train_total))

        model.eval()
        test_total = 0
        test_loss = 0
        test_correct = 0

        with torch.no_grad():
            for i, (test_input, target) in enumerate(val_loader):
                input_var = torch.autograd.Variable(test_input.cuda())
                target_var = torch.autograd.Variable(target.cuda())
                output = model(input_var)
                _, test_predicted = torch.max(output.data, 1)
                loss = criterion(output, target_var)
                test_loss += loss.item()
                test_total += target.size(0)
                test_correct += (test_predicted == target_var.data).sum()

        acc = 100 * test_correct / test_total
        if max_acc < acc:
            max_acc = acc

        print('test %d epoch loss: %.3f  acc: %.3f  load:%d' % (
            epoch, test_loss / test_total, 100 * test_correct / test_total, 1))
        f = open('./experiment_record(first)/' + model_name + '/result.txt', "a")
        f.write('test  %d epoch loss: %.3f  acc: %.3f\n' %
                (epoch + 1, test_loss / test_total, acc))
        f.close()

    return max_acc


if __name__ == '__main__':
    main()
