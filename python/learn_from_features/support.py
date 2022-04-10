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
import re
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
def save_net(net, epoch, model_name):
    save_epoch = ('./pkl/' + model_name + '/epoch_%d_net' % epoch)
    torch.save(net, save_epoch + '.pkl')  # 保存整个网络
    torch.save(net.state_dict(), save_epoch + '_params.pkl')  # 只保存网络中的参数 (速度快, 占内存少)
    print('save_done')


# 提取网络
def load_net(net):
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
def train(net, epochs, lr, train_loader, test_loader, model_name, weight_decay=5e-4):
    # 刷新txt
    net.train()
    with open('./experiment_record/' + model_name + '/result.txt', "w") as f:
        f.write("开始实验\n")  # 自带文件关闭功能，不需要再写f.close()

    # 定义loss和optimizer
    cirterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=lr, momentum=0.9, weight_decay=weight_decay)
    scheduler = optim.lr_scheduler.MultiStepLR(optimizer=optimizer, milestones=[50, 100, 150], gamma=0.1)
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
            inputs, train_labels, name = data
            # inputs, train_labels = data
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
        f = open('./experiment_record/' + model_name + '/result.txt', "a")
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
                testimages, testlabels, name = data
                # testimages, testlabels = data
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
        f = open('./experiment_record/' + model_name + '/result.txt', "a")
        f.write('test  %d epoch loss: %.3f  acc: %.3f  load:%d\n' %
                (epoch + 1, test_loss / test_total, acc, loadingtime2))
        f.close()

        scheduler.step()

        if (epoch + 1) / 50 == 1:
            print('epoch decrease 10x')
            save_net(net, epoch, model_name)
        if (epoch + 1) / 100 == 1:
            print('epoch decrease 10x')
            save_net(net, epoch, model_name)
        if (epoch + 1) / 150 == 1:
            print('epoch decrease 10x')
            save_net(net, epoch, model_name)
        if (epoch + 1) / 200 == 1:
            save_net(net, epoch, model_name)

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
    f = open('./experiment_record/' + model + '/final_result.txt', "a")
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


def select_sample(net, test_loader):
    # 模型test
    correct = 0
    test_total = 0
    right_sample = {}
    same_sample = {}
    # net.eval()
    with torch.no_grad():
        for data in test_loader:
            testimages, testlabels, name = data
            testimages, testlabels = Variable(testimages), Variable(testlabels)
            testimages, testlabels = testimages.cuda(), testlabels.cuda()
            outputs = net(testimages)
            _, test_predicted = torch.max(outputs.data, 1)

            test_total += testlabels.size(0)
            correct += (test_predicted == testlabels.data).sum()
            for i in range(testlabels.data.size(0)):
                if test_predicted[i] == testlabels.data[i]:
                    right_sample[name[i]] = outputs[i][test_predicted[i]]

    for i in range(100):
        for k, v in (right_sample.items()):
            if (int((re.findall('./dataset/train/(.*)/', k))[0])) == i:
                same_sample[k] = v
        best_sample = sorted(same_sample.items(), key=lambda x: x[1], reverse=True)

        with open('./dataset/select_train.txt', 'a') as f1:
            for q in range(50):
                f1.write('%s\t%f\n' % (best_sample[q][0], best_sample[q][1]))

        best_sample.clear()


def train_apart(net1, net2, net3, net4, epochs, lr, train_loader, test_loader, model_name1, model_name2, weight_decay=5e-4):
    # 刷新txt
    net2.train()
    net4.train()
    with open('./experiment_record/' + model_name2 + '/result.txt', "w") as f:
        f.write("开始实验\n")  # 自带文件关闭功能，不需要再写f.close()

    # 定义loss和optimizer
    cirterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net2.parameters(), lr=lr, momentum=0.9, weight_decay=weight_decay)
    scheduler = optim.lr_scheduler.MultiStepLR(optimizer=optimizer, milestones=[50, 100, 150], gamma=0.1)
    optimizer1 = optim.SGD(net4.parameters(), lr=lr, momentum=0.9, weight_decay=weight_decay)
    scheduler1 = optim.lr_scheduler.MultiStepLR(optimizer=optimizer1, milestones=[50, 100, 150], gamma=0.1)
    max_acc = 0
    loadingtime = 0
    loadingtime2 = 0

    for epoch in range(epochs):

        # 训练开始
        running_loss = 0.0
        running_loss1 = 0.0
        train_total = 0
        train_correct = 0
        print("yes\n")
        starttime = datetime.datetime.now()
        for i, data in enumerate(train_loader, 0):
            inputs, train_labels, name = data
            # inputs, train_labels = data
            inputs, labels = Variable(inputs), Variable(train_labels)
            inputs, labels = inputs.cuda(), labels.cuda()
            optimizer.zero_grad()
            outputs1 = net1(inputs)
            outputs2 = net2(inputs)
            # loss = cirterion(outputs1, outputs2)
            loss = cirterion(outputs1, outputs2.long())

            optimizer1.zero_grad()
            outputs3 = net3(outputs1)
            outputs4 = net4(outputs1)
            # outputs3 = net4(outputs2)
            _, train_predicted = torch.max(outputs4.data, 1)
            train_correct += (train_predicted == labels.data).sum()
            # loss1 = cirterion(outputs3, outputs4)
            loss1 = cirterion(outputs3, outputs4.long())

            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            loss1.backward()
            optimizer1.step()
            running_loss1 += loss1.item()
            train_total += train_labels.size(0)

        endtime = datetime.datetime.now()
        loadingtime = (endtime - starttime).seconds

        print('train %d epoch loss1: %.3f loss2: %.3f acc: %.3f  load:%d' % (
            epoch + 1, running_loss / train_total, running_loss1 / train_total, 100 * train_correct / train_total, loadingtime))
        f = open('./experiment_record/' + model_name2 + '/result.txt', "a")
        f.write('train %d epoch loss1: %.3f loss2: %.3f acc: %.3f  load:%d \n' % (
            epoch + 1, running_loss / train_total, running_loss1 / train_total, 100 * train_correct / train_total, loadingtime))
        f.close()

        correct = 0
        test_loss = 0.0
        test_total = 0
        net2.eval()
        net4.eval()
        with torch.no_grad():
            for data in test_loader:
                testimages, testlabels, name = data
                # testimages, testlabels = data
                testimages, testlabels = Variable(testimages), Variable(testlabels)
                testimages, testlabels = testimages.cuda(), testlabels.cuda()
                outputs5 = net2(testimages)
                outputs6 = net4(outputs5)

                loss2 = cirterion(outputs6, testlabels.long())
                _, test_predicted = torch.max(outputs6.data, 1)
                test_loss += loss2.item()
                test_total += testlabels.size(0)
                correct += (test_predicted == testlabels.data).sum()

        endtime2 = datetime.datetime.now()
        loadingtime2 = (endtime2 - endtime).seconds
        acc = 100 * correct / test_total
        if max_acc < acc:
            max_acc = acc
        # 打印测试结果n
        print('test  %d epoch  loss: %.3f  acc: %.3f  load:%d ' %
              (epoch + 1, test_loss / test_total, acc, loadingtime2))
        f = open('./experiment_record/' + model_name2 + '/result.txt', "a")
        f.write('test  %d epoch  loss: %.3f  acc: %.3f  load:%d\n' %
                (epoch + 1, test_loss / test_total, acc, loadingtime2))
        f.close()

        scheduler.step()
        scheduler1.step()

        if (epoch + 1) / 50 == 1:
            print('epoch decrease 10x')
            save_net(net2, epoch, model_name1)
            save_net(net4, epoch, model_name2)
        if (epoch + 1) / 100 == 1:
            print('epoch decrease 10x')
            save_net(net2, epoch, model_name1)
            save_net(net4, epoch, model_name2)
        if (epoch + 1) / 150 == 1:
            print('epoch decrease 10x')
            save_net(net2, epoch, model_name1)
            save_net(net4, epoch, model_name2)
        if (epoch + 1) / 200 == 1:
            save_net(net2, epoch, model_name1)
            save_net(net4, epoch, model_name2)

    return max_acc, loadingtime, loadingtime2
