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
from torchvision import transforms
import torchvision.models as models
import torch.optim as optim
import datetime
from torch.autograd import Variable


# 保存网络
def save_net(net, epoch):
    save_epoch = ('./pkl/epoch_%d_net' % epoch)
    torch.save(net, save_epoch + '.pkl')  # 保存整个网络
    torch.save(net.state_dict(), './pkl/net_params.pkl')  # 只保存网络中的参数 (速度快, 占内存少)
    print('save_done')


# 提取网络
def load_net(net):
    # restore entire net1 to net2
    net = torch.load(net + '_net.pkl')
    return net


# 图像归一化后裁剪，最后尺寸224*224*3
def datatransform():
    data_transform = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.24703223, 0.24348512, 0.26158784])
    ])
    return data_transform


def transform_test():
    test_transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return test_transform


# 定义训练过程
def train(net, epochs, lr, train_loader, test_loader):
    # 刷新txt
    lr_decay = [80, 100, 120, 140]
    net.train()
    with open("result.txt", "w") as f:
        f.write("开始实验")  # 这句话自带文件关闭功能，不需要再写f.close()

    # 定义loss和optimizer
    cirterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=lr, momentum=0.9, weight_decay=5e-4)

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
        f = open("result.txt", "a")
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
                _, predicted = torch.max(outputs.data, 1)
                loss = cirterion(outputs, testlabels)
                test_loss += loss.item()
                test_total += testlabels.size(0)
                correct += (predicted == testlabels.data).sum()

        # 测试计时
        endtime2 = datetime.datetime.now()
        loadingtime2 = (endtime2 - endtime).seconds

        # 打印测试结果
        print('test  %d epoch loss: %.3f  acc: %.3f ' %
              (epoch + 1, test_loss / test_total, 100 * correct / test_total))
        f = open("result.txt", "a")
        f.write('test  %d epoch loss: %.3f  acc: %.3f  load:%d\n' %
                (epoch + 1, test_loss / test_total, 100 * correct / test_total, loadingtime2))
        f.close()

        # if (epoch + 1) % 50 == 0:
        #     lr = lr / 10
        #     save_net(net, epoch)
        if epoch in lr_decay:
            for p in optimizer.param_groups:
                p['lr'] *= 0.1


def loadmodel(num_classes=10):
    net = models.mobilenet_v2(pretrained=False)
    net.classifier = nn.Sequential(
        nn.Dropout(0.2),
        nn.Linear(in_features=1280, out_features=num_classes, bias=True))
    return net
