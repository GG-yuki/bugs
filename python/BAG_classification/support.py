# -*- coding: utf-8 -*-
'''
/********************************************************************
*
*  文件名：support.py
*
*  文件描述：封装类
*
*  创建人： qiwei_ji, 2020年11月20日
*
*  版本号：1.0
*
*  修改记录：0
*
********************************************************************/
'''
import torch
import torch.nn as nn
from torchvision import transforms
import torch.optim as optim
import datetime
import torchvision.models as models
from torch.autograd import Variable


# 载入模型
def loadmodel(num_classes = 2):
    # 定义是否使用GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net = models.resnet18(pretrained=False).to(device)
    num_fc_ftr = net.fc.in_features
    net.fc = torch.nn.Linear(num_fc_ftr, num_classes).to(device)
    return net


# 保存网络
def save_net(net):
    torch.save(net, 'net.pkl')  # 保存整个网络
    torch.save(net.state_dict(), 'net_params.pkl')   # 只保存网络中的参数 (速度快, 占内存少)
    print('save_done')


# 提取网络
def restore_net():
    # restore entire net1 to net2
    net = torch.load('net.pkl')
    torch.save(net.state_dict(), 'net_params.pkl')  # 只保存网络中的参数 (速度快, 占内存少)
    return net


# 图像归一化后裁剪，最后尺寸224*224*3
def datatransform():
    data_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return data_transform


# 定义训练过程
def train(net,epochs,LR,train_loader,test_loader):

    # 定义是否使用GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 定义loss和optimizer
    cirterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=LR, momentum=0.9)

    for epoch in range(epochs):
        starttime = datetime.datetime.now() # 计时

        # 训练开始
        # net = net.train()
        running_loss = 0.0
        train_correct = 0
        train_total = 0
        print("yes\n")
        for i, data in enumerate(train_loader, 0):
            inputs, train_labels = data
            inputs, labels = Variable(inputs), Variable(train_labels)
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = net(inputs)
            train_predicted = torch.max(outputs.data, 1)[1]
            # _, train_predicted = torch.max(outputs.data, 1)
            # print(train_predicted,labels.data)
            train_correct += (train_predicted == labels.data).sum()
            loss = cirterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            train_total += train_labels.size(0)

        # 训练计时
        endtime = datetime.datetime.now()
        loadingtime=(endtime - starttime).seconds
        # print(loadingtime)

        # 打印训练结果
        print('train %d epoch loss: %.3f  acc: %.3f  load:%d' % (
            epoch + 1, running_loss / train_total, 100 * train_correct / train_total,loadingtime))
        f = open("foo.txt", "a")
        f.write('train %d epoch loss: %.3f  acc: %.3f  load:%d \n' % (
            epoch + 1, running_loss / train_total, 100 * train_correct / train_total,loadingtime))
        f.close()

        # 模型test
        correct = 0
        test_loss = 0.0
        test_total = 0
        # net.eval()

        for data in test_loader:
            testimages, testlabels = data
            testimages, testlabels = Variable(testimages), Variable(testlabels)
            testimages, testlabels = testimages.to(device), testlabels.to(device)
            net =net.eval()
            outputs = net(testimages)
            predicted = torch.max(outputs.data, 1)[1]
            # _, predicted = torch.max(outputs.data, 1)
            # print(predicted,testlabels)
            loss = cirterion(outputs, testlabels)
            test_loss += loss.item()
            test_total += testlabels.size(0)
            correct += (predicted == testlabels.data).sum()

        # 测试计时
        endtime2 = datetime.datetime.now()
        loadingtime2=(endtime2 - endtime).seconds
        # print(loadingtime2)

        # 打印测试结果
        print('test  %d epoch loss: %.3f  acc: %.3f ' % (epoch + 1, test_loss / test_total, 100 * correct / test_total))
        f = open("foo.txt", "a")
        f.write('test  %d epoch loss: %.3f  acc: %.3f  load:%d\n' % (epoch + 1, test_loss / test_total, 100 * correct / test_total,loadingtime2))
        f.close()

        if epoch % 30 == 0:
            LR=LR/10

