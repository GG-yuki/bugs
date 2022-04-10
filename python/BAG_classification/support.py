# -*- coding: utf-8 -*-
'''
/********************************************************************
*
*  文件名：support.py
*
*  文件描述：封装类
*
*  创建人： qiwei_ji, 2020年11月23日
*
*  版本号：2.0
*
*  修改记录：2
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
import numpy as np
import matplotlib.pyplot as plt
from torchvision import utils


# 载入模型
def loadmodel(num_classes=2):
    # 定义是否使用GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net = models.resnet18(pretrained=False).to(device)
    num_fc_ftr = net.fc.in_features
    net.fc = torch.nn.Linear(num_fc_ftr, num_classes).to(device)
    return net


def loadresnet50():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net = models.resnet50(pretrained=False).to(device)
    num_fc_ftr = net.fc.in_features
    net.fc = torch.nn.Linear(num_fc_ftr, 2).to(device)
    return net


# 保存网络
def save_18(net):
    torch.save(net, 'resnet18.pkl')  # 保存整个网络
    torch.save(net.state_dict(), 'resnet18_params.pkl')  # 只保存网络中的参数 (速度快, 占内存少)
    print('save_done')


'''
/********************************************************************/
'''
# 提取网络
def restore_18():
    # restore entire net1 to net2
    net = torch.load(r'resnet18.pkl',map_location='cpu')
    return net


'''
/********************************************************************/
'''
def save_50(net):
    torch.save(net, 'resnet50.pkl')  # 保存整个网络
    torch.save(net.state_dict(), 'resnet50_params.pkl')  # 只保存网络中的参数 (速度快, 占内存少)
    print('save_done')


# 提取网络
def restore_50():
    # restore entire net1 to net2
    net = torch.load('resnet50.pkl',map_location='cpu')
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


def imshow(inp, pred, ylabel,number):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)
    plt.title('GroundTruth: {}, Predicted: {}'.format(ylabel, pred))
    plt.savefig(r'./result/%d.jpg'%number)


# 加载网络后进行预测
def test(net, test_loader):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net = net.to(device)
    correct_test = 0
    total_test = 0
    i = 1
    # plt.figure()
    for data in test_loader:
        images, labels = data
        out = utils.make_grid(images)
        images, labels = images.to(device), labels.to(device)
        net = net.eval()
        outputs = net(images)
        predicted = torch.max(outputs.data, 1)[1]
        print(labels.item())
        # plt.subplot(1, 1, 1)
        # if (predicted.numpy()[0] == 0):
        #     preclassstr = 'boy'
        # else:
        #     preclassstr = 'girl'
        # if (labels.numpy()[0] == 0):
        #     labelclassstr = 'boy'
        # else:
        #     labelclassstr = 'girl'
        # imshow(out, preclassstr, labelclassstr,i)
        i = i+1
        total_test += labels.size(0)
        correct_test += (predicted == labels).sum()
        # plt.clf()
    # plt.close()
    print('测试准确率为: %d %%' % ((100 * correct_test // total_test)))



# 定义训练过程
def train(net, epochs, LR, train_loader, test_loader):
    # 定义是否使用GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 定义loss和optimizer
    cirterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=LR, momentum=0.9)
    j = 1
    for epoch in range(epochs):
        starttime = datetime.datetime.now()  # 计时

        # 训练开始
        # net = net.train()
        j = j+1
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
            train_correct += (train_predicted == labels.data).sum()
            loss = cirterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            train_total += train_labels.size(0)


        # 打印训练结果
        print('train %d epoch loss: %.3f acc: %.3f' % (
            epoch + 1, running_loss / train_total, 100 * train_correct / train_total))
        f = open("result_train.txt", "a")
        f.write('train %d epoch loss: %.3f acc: %.3f \n' % (
            epoch + 1, running_loss / train_total, 100 * train_correct / train_total))
        f.close()


        a = 0
        correct_test = 0
        total_test = 0
        if j % 5 == 0:
            plt.figure()
        for data in test_loader:
            images, labels = data
            out = utils.make_grid(images)
            images, labels = images.to(device), labels.to(device)
            net = net.eval()
            outputs = net(images)
            predicted = torch.max(outputs.data, 1)[1]
            print(predicted)

            predicted = predicted.cpu()
            labels = labels.cpu()

            if j % 5 == 0:
                plt.subplot(1, 1, 1)
            if (predicted.numpy()[0] == 0):
                preclassstr = 'boy'
            else:
                preclassstr = 'girl'
            if (labels.numpy()[0] == 0):
                labelclassstr = 'boy'
            else:
                labelclassstr = 'girl'
            if j % 5 == 0:
                imshow(out, preclassstr, labelclassstr, a)
                plt.clf()
            a = a + 1
            total_test += labels.size(0)
            correct_test += (predicted == labels).sum()
        if j % 5 == 0:
            plt.close()


        # 打印测试结果
        print('test  %d epoch  acc: %.3f ' % (
            epoch + 1, 100 * correct_test / total_test))
        f = open("result_test.txt", "a")
        f.write('test  %d epoch  acc: %.3f \n' % (
            epoch + 1, 100 * correct_test / total_test))
        f.close()

        # 每15轮，lr缩小10倍
        if epoch % 15 == 0:
            LR = LR / 10
