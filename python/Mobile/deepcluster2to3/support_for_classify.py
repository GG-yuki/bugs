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
from torchvision import transforms, datasets
import torch.optim as optim
import datetime
from torch.autograd import Variable
import numpy as np
from typing import Optional
from mobilenetv1_sobel import *


# 保存网络
def save_net(net, epoch):
    save_epoch = ('./pkl/epoch_%d_net' % epoch)
    torch.save(net, save_epoch + '.pkl')  # 保存整个网络
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

        scheduler.step()

        if (epoch + 1) / 50 == 1:
            print('epoch decrease 10x')
            save_net(net, epoch)
        if (epoch + 1) / 100 == 1:
            print('epoch decrease 10x')
            save_net(net, epoch)
        if (epoch + 1) / 150 == 1:
            print('epoch decrease 10x')
            save_net(net, epoch)
        if (epoch + 1) / 200 == 1:
            print('epoch decrease 10x')
            save_net(net, epoch)

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


def write_result(model, epochs, batch_size, num_workers, lr, max_acc, weight_decay, traintime, testtime):
    f = open('./experiment_record(first)/' + model + '/final_result.txt', "a")
    f.write('model %s   train %d epoch   batch_size %d   num_workers %d   lr %f   max_acc: %.3f  '
            'weight_decay %f   traintime %d   testtime %d\n' %
            (model, epochs, batch_size, num_workers, lr, max_acc, weight_decay, traintime, testtime))
    f.close()


class Data_loader:

    def __init__(self, num_workers, batch_size):
        # self.root = root
        self.num_workers = num_workers
        self.batch_size = batch_size
        self.train_transform = train_transform()
        self.test_transform = test_transform()

    def trainloader(self):
<<<<<<< HEAD
        train_dataset = datasets.ImageFolder(root=r'./apart_dataset/50/train', transform=self.train_transform)
=======
        train_dataset = datasets.ImageFolder(root=r'./dataset/50_train', transform=self.train_transform)
>>>>>>> a240ef68 (first commit)
        train_loader = torch.utils.data.DataLoader(train_dataset,
                                                   batch_size=self.batch_size,
                                                   shuffle=True,
                                                   num_workers=self.num_workers)
        return train_loader

    def testloader(self):
<<<<<<< HEAD
        test_dataset = datasets.ImageFolder(root=r'./apart_dataset/full/test', transform=self.test_transform)
=======
        test_dataset = datasets.ImageFolder(root=r'./dataset/test', transform=self.test_transform)
>>>>>>> a240ef68 (first commit)
        test_loader = torch.utils.data.DataLoader(test_dataset,
                                                  batch_size=self.batch_size,
                                                  shuffle=True,
                                                  num_workers=self.num_workers)
        return test_loader


<<<<<<< HEAD
def load_model(path=r'./exp/checkpoint.pth.tar'):
=======
def load_model(path=r'./exp/checkpoint_mobilenetv1.pth.tar'):
>>>>>>> a240ef68 (first commit)
    """Loads model and return it without DataParallel table."""
    if True:
        print(("=> loading checkpoint '{}'".format(path)))
        checkpoint = torch.load(path)

        # size of the top layer
        n = checkpoint['state_dict']['top_layer.bias'].size()

        # build skeleton of the model
        sob = 'sobel.0.weight' in list(checkpoint['state_dict'].keys())
        model = MobileNetV1(sobel=sob, num_classes=int(n[0]))

        # deal with a dataparallel table
        def rename_key(key):
            if not 'module' in key:
                return key
            return ''.join(key.split('.module'))

        checkpoint['state_dict'] = {rename_key(key): val
                                    for key, val
                                    in list(checkpoint['state_dict'].items())}

        # load weights
        model.load_state_dict(checkpoint['state_dict'])
        print("Loaded")
    return model


class Classifier(torch.nn.Module):
    def __init__(self, in_channels, num_classes):
        super().__init__()
        self.conv = torch.nn.Conv2d(
                in_channels=in_channels,
                out_channels=num_classes,
                kernel_size=1,
                bias=True)

    def forward(self, x):
        x = x.view(x.size(0), 1024, 1, 1)
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        return x

    def init_params(self):
        torch.nn.init.xavier_normal_(self.conv.weight, gain=1.0)
