"""
/********************************************************************
*
*  文件名：support.py
*
*  文件描述：封装类
*
*  创建人： qiwei_ji, 2020年10月4日
*
*  版本号：1.2
*
*  修改记录：64
*
********************************************************************/
"""
import torch
import torch.nn as nn
from torchvision import transforms, datasets
import torchvision.models as models
import torch.optim as optim
import datetime
from torch.autograd import Variable
import numpy as np
from typing import Optional


# 保存网络
def save_net(net, epoch):
    save_epoch = ('./pkl/epoch_%d_net' % epoch)
    # torch.save(net, save_epoch + '.pkl')  # 保存整个网络
    torch.save(net.state_dict(), './pkl/net_params.pkl')  # 只保存网络中的参数 (速度快, 占内存少)
    print('save_done')


# 提取网络
def load_net(net):
    # restore entire net1 to net2
    model_load = torch.load('./pkl/epoch_' + net + '_net.pkl')
    return model_load


# 图像归一化后裁剪，最后尺寸224*224*3
def train_transform():
    data_transform = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
    ])
    return data_transform


def test_transform():
    data_transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    return data_transform


# 定义训练过程
def train(net, epochs, lr, train_loader, test_loader, weight_decay=5e-4):
    # 刷新txt
    model_name = format(net.__class__.__name__)
    net.train()
    with open('./experiment_record(first)/' + model_name + '/result.txt', "w") as f:
        f.write("开始实验\n")  # 自带文件关闭功能，不需要再写f.close()

    # 定义loss和optimizer
    cirterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=lr, momentum=0.9, weight_decay=weight_decay)
    scheduler = optim.lr_scheduler.MultiStepLR(optimizer=optimizer, milestones=[40, 60, 80], gamma=0.1)
    max_acc = 0
    loadingtime = 0
    loadingtime2 = 0

    for epoch in range(epochs):
        starttime = datetime.datetime.now()  # 计时

        # 训练开始
        running_loss = 0.0
        train_correct = 0
        train_total = 0
        print("yes\n")
        for i, data in enumerate(train_loader, 0):
            inputs, train_labels = data
            inputs, labels = Variable(inputs), Variable(train_labels)
            inputs, labels = inputs.cuda(), labels.cuda()
            optimizer.zero_grad()
            outputs = net(inputs)
            loss = cirterion(outputs, labels.long())
            _, train_predicted = torch.max(outputs.data, 1)
            train_correct += (train_predicted == labels.data).sum()
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            train_total += train_labels.size(0)

        # 训练计时
        endtime = datetime.datetime.now()
        loadingtime = (endtime - starttime).seconds

        # 打印训练结果
        print('train %d epoch loss: %.3f  acc: %.3f  load:%d' % (
            epoch + 1, running_loss / train_total, 100 * train_correct / train_total, loadingtime))
        f = open('./experiment_record(first)/' + model_name + '/result.txt', "a")
        f.write('train %d epoch loss: %.3f  acc: %.3f  load:%d \n' % (
            epoch + 1, running_loss / train_total, 100 * train_correct / train_total, loadingtime))
        f.close()

        # 模型test
        correct = 0
        test_loss = 0.0
        test_total = 0
        net.eval()
        with torch.no_grad():
            for data in test_loader:
                testimages, testlabels = data
                testimages, testlabels = Variable(testimages), Variable(testlabels)
                testimages, testlabels = testimages.cuda(), testlabels.cuda()
                net = net.eval()
                outputs = net(testimages)
                loss = cirterion(outputs, testlabels.long())
                _, test_predicted = torch.max(outputs.data, 1)
                test_loss += loss.item()
                test_total += testlabels.size(0)
                correct += (test_predicted == testlabels.data).sum()

        # 测试计时
        endtime2 = datetime.datetime.now()
        loadingtime2 = (endtime2 - endtime).seconds
        acc = 100 * correct / test_total
        if max_acc < acc:
            max_acc = acc
        # 打印测试结果n
        print('test  %d epoch loss: %.3f  acc: %.3f  load:%d ' %
              (epoch + 1, test_loss / test_total, acc, loadingtime2))
        f = open('./experiment_record(first)/' + model_name + '/result.txt', "a")
        f.write('test  %d epoch loss: %.3f  acc: %.3f  load:%d\n' %
                (epoch + 1, test_loss / test_total, acc, loadingtime2))
        f.close()
        print(max_acc)

        scheduler.step()

        if epoch == 0:
            print('epoch decrease 10x')
            save_net(net, epoch)

        if (epoch + 1) / 40 == 1:
            print('epoch decrease 10x')
            save_net(net, epoch+1)
        if (epoch + 1) / 60 == 1:
            print('epoch decrease 10x')
            save_net(net, epoch+1)
        if (epoch + 1) / 80 == 1:
            print('epoch decrease 10x')
            save_net(net, epoch+1)

    return max_acc, loadingtime, loadingtime2


def set_random_seed(seed: Optional[int] = None) -> int:
    """
    Set the random seed for numpy and torch.
    Parameters
    ----------
    seed: int or None, default None
        Specify initial random seed.
    Returns
    -------
    seed : int
    """
    seed = np.random.randint(10_000) if seed is None else seed
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # type: ignore
    return seed


def load_model(num_classes=10):
    net = models.mobilenet_v2(pretrained=False)
    net.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_features=1280, out_features=num_classes, bias=True))
    return net


def write_result(model, epochs, batch_size, num_workers, lr, max_acc, weight_decay, traintime, testtime):
    f = open('./experiment_record(first)/' + model + '/final_result.txt', "a")
    f.write('model %s   train %d epoch   batch_size %d   num_workers %d   lr %f   max_acc: %.3f  '
            'weight_decay %f   traintime %d   testtime %d\n' %
            (model, epochs, batch_size, num_workers, lr, max_acc, weight_decay, traintime, testtime))
    f.close()


class Data_loader:

    def __init__(self, root, num_workers, batch_size):
        self.root = root
        self.num_workers = num_workers
        self.batch_size = batch_size
        self.train_transform = train_transform()
        self.test_transform = test_transform()

    def trainloader(self):
        train_dataset = datasets.CIFAR100(root=self.root, train=True, transform=self.train_transform, download=True)
        train_loader = torch.utils.data.DataLoader(train_dataset,
                                                   batch_size=self.batch_size,
                                                   shuffle=True,
                                                   num_workers=self.num_workers)
        return train_loader

    def testloader(self):
        test_dataset = datasets.CIFAR100(root=self.root, train=False, transform=self.test_transform, download=True)
        test_loader = torch.utils.data.DataLoader(test_dataset,
                                                  batch_size=self.batch_size,
                                                  shuffle=True,
                                                  num_workers=self.num_workers)
        return test_loader


class Data_loader10:

    def __init__(self, root, num_workers, batch_size):
        self.root = root
        self.num_workers = num_workers
        self.batch_size = batch_size
        self.train_transform = train_transform()
        self.test_transform = test_transform()

    def trainloader(self):
        train_dataset = datasets.CIFAR10(root=self.root, train=True, transform=self.train_transform, download=True)
        train_loader = torch.utils.data.DataLoader(train_dataset,
                                                   batch_size=self.batch_size,
                                                   shuffle=True,
                                                   num_workers=self.num_workers)
        return train_loader

    def testloader(self):
        test_dataset = datasets.CIFAR10(root=self.root, train=False, transform=self.test_transform, download=True)
        test_loader = torch.utils.data.DataLoader(test_dataset,
                                                  batch_size=self.batch_size,
                                                  shuffle=True,
                                                  num_workers=self.num_workers)
        return test_loader