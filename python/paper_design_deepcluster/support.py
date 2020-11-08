'''
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
'''
import torch
import torch.nn as nn
from torchvision import transforms
import torch.optim as optim
import datetime
import os
import numpy as np
from torch.autograd import Variable


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


# 提取网络(不常用，用的时候记得修改）
def restore_params():
    # 新建 net2
    net2 = mobilenetv2.mobilenetv2(num_classes=2)
    # 将保存的参数复制到 net2
    net2.load_state_dict(torch.load('net_params.pkl'))
    return net2


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

    # 定义loss和optimizer
    cirterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=LR, momentum=0.9)

    for epoch in range(epochs):
        starttime = datetime.datetime.now() # 计时

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
            _, train_predicted = torch.max(outputs.data, 1)
            # print(train_predicted,labels.data)
            train_correct += (train_predicted == labels.data).sum()
            loss = cirterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            train_total += train_labels.size(0)
            print("%d\n"%(i))

        # 训练计时
        endtime = datetime.datetime.now()
        loadingtime=(endtime - starttime).seconds
        print(loadingtime)

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
        net.eval()

        for data in test_loader:
            testimages, testlabels = data
            testimages, testlabels = Variable(testimages), Variable(testlabels)
            testimages, testlabels = testimages.cuda(), testlabels.cuda()
            net =net.eval()
            outputs = net(testimages)
            print(outputs)
            _, predicted = torch.max(outputs.data, 1)
            print(predicted,testlabels)
            loss = cirterion(outputs, testlabels)
            test_loss += loss.item()
            test_total += testlabels.size(0)
            correct += (predicted == testlabels.data).sum()

        # 测试计时
        endtime2 = datetime.datetime.now()
        loadingtime2=(endtime2 - endtime).seconds
        print(loadingtime2)

        # 打印测试结果
        print('test  %d epoch loss: %.3f  acc: %.3f ' % (epoch + 1, test_loss / test_total, 100 * correct / test_total))
        f = open("foo.txt", "a")
        f.write('test  %d epoch loss: %.3f  acc: %.3f  load:%d\n' % (epoch + 1, test_loss / test_total, 100 * correct / test_total,loadingtime2))
        f.close()

        if epoch == 30:
            LR=LR/10
        if epoch == 60:
            LR=LR/10


def shuffle_data():
    original_dataset_dir = r'/home/jijl/My_project/graduation_design/sdsds/test'
    total_num = int(len(os.listdir(original_dataset_dir)) / 2)
    random_idx = np.array(range(total_num))
    np.random.shuffle(random_idx)