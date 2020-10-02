# coding=utf-8
import os
import torch.optim as optim
from torch.utils.data import Dataset
import datetime
from support import *
from mobilenetv1 import *
from mobilenetv2 import *
from mobilenetv3 import *


# 训练参数参数
epochs = 60 # 训练次数
batch_size = 64  # 批处理大小
num_workers = 0  # 多线程的数目
LR=0.001


# kaggle原始数据集地址
# original_dataset_dir = r'sdsds\train'
original_dataset_dir = r'/home/jijl/My_project/graduation_design/sdsds/train'
total_num = int(len(os.listdir(original_dataset_dir)) / 2)
random_idx = np.array(range(total_num))
np.random.shuffle(random_idx)
print(total_num)


# 对加载的图像作归一化处理， 并裁剪为[224x224x3]大小的图像
data_transform=datatransform()


#加载数据
train_dataset = datasets.ImageFolder(root=r'/home/jijl/My_project/graduation_design/sdsds/train',
                                     transform=data_transform)
# train_dataset = datasets.ImageFolder(root=r'sdsds\train',
#                                      transform=data_transform)
train_loader = torch.utils.data.DataLoader(train_dataset,
                                           batch_size=batch_size,
                                           shuffle=True,
                                           num_workers=num_workers)
test_dataset = datasets.ImageFolder(root=r'/home/jijl/My_project/graduation_design/sdsds/test', transform=data_transform)
# test_dataset = datasets.ImageFolder(root=r'sdsds\test', transform=data_transform)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)


#网络实例化
# net=restore_params()
net = MobileNet2(1000)


# 定义loss和optimizer
cirterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=LR, momentum=0.9)


def train(LR):
    for epoch in range(epochs):
        starttime = datetime.datetime.now()
        running_loss = 0.0
        train_correct = 0
        train_total = 0
        print("yes\n")
        for i, data in enumerate(train_loader, 0):
            inputs, train_labels = data
            inputs, labels = Variable(inputs), Variable(train_labels)
            optimizer.zero_grad()
            outputs = net(inputs)
            _, train_predicted = torch.max(outputs.data, 1)
            train_correct += (train_predicted == labels.data).sum()
            loss = cirterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            train_total += train_labels.size(0)
            print("%d\n"%(i))
        endtime = datetime.datetime.now()
        loadingtime=(endtime - starttime).seconds
        print(loadingtime)
        print('train %d epoch loss: %.3f  acc: %.3f  load:%d' % (
            epoch + 1, running_loss / train_total, 100 * train_correct / train_total,loadingtime))
        f = open("foo.txt", "a")
        f.write('train %d epoch loss: %.3f  acc: %.3f  load:%d \n' % (
            epoch + 1, running_loss / train_total, 100 * train_correct / train_total,loadingtime))
        f.close()
        # 模型测试
        correct = 0
        test_loss = 0.0
        test_total = 0
        net.eval()
        for data in test_loader:
            images, labels = data
            images, labels = Variable(images), Variable(labels)
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            loss = cirterion(outputs, labels)
            test_loss += loss.item()
            test_total += labels.size(0)
            correct += (predicted == labels.data).sum()
        endtime2 = datetime.datetime.now()
        loadingtime2=(endtime2 - endtime).seconds
        print(loadingtime2)
        print('test  %d epoch loss: %.3f  acc: %.3f ' % (epoch + 1, test_loss / test_total, 100 * correct / test_total))
        f = open("foo.txt", "a")
        f.write('test  %d epoch loss: %.3f  acc: %.3f  load:%d\n' % (epoch + 1, test_loss / test_total, 100 * correct / test_total,loadingtime2))
        f.close()
        if epoch == 10:
            LR=LR/10
        if epoch == 30:
            LR=LR/10


train(LR)


def save_net(meet):
    torch.save(meet, 'net.pkl')  # 保存整个网络
    torch.save(meet.state_dict(), 'net_params.pkl')   # 只保存网络中的参数 (速度快, 占内存少)
    print('save_done')

save_net(net)
