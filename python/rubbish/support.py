'''
/********************************************************************
*
*  文件名：support.py
*
*  文件描述：封装类
*
*  创建人： qiwei_ji, 2020年5月31日
*
*  版本号：1.1.3.0301_alpha
*
*  修改记录：63
*
********************************************************************/
'''


import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.utils.data as Data
import csv
from torchvision import datasets,transforms, models
import mobilenetv2

'''
/*============================================================
*
* 函 数 名：loadTrainData()
*
* 参  数：
*
*    None
*
* 功能描述:
*
*    载入excel数据
*
* 返 回 值：42000*28*28的train数据
*
* 抛出异常：
*
* 作  者：qiwei_ji 2020/1/12
* ============================================================*/
'''
def loadTrainData():
    l=[]
    with open('train.csv') as file:
         lines=csv.reader(file)
         for line in lines:
             l.append(line) #42001*785
    l.remove(l[0])
    l=np.array(l)
    # label=l[:,0]
    # data=l[:,1:]
    temp=l[2,1:785]
    # return toInt(data),toInt(label)
    return toInt(temp)


'''
/*============================================================
*
* 函 数 名：toInt()
*
* 参  数：
*
*    numpy矩阵
*
* 功能描述:
*
*    字符串转换成数字
*
* 返 回 值：数字矩阵
*
* 抛出异常：
*
* 作  者：qiwei_ji 2020/1/14
* ============================================================*/
'''
def toInt(array):
    array=np.mat(array)
    m,n=np.shape(array)
    newArray=np.zeros((m,n))
    for i in range(m):
        for j in range(n):
                newArray[i,j]=int(array[i,j])
    return newArray


#保存网络
def save_net(net):
    torch.save(net, 'net.pkl')  # 保存整个网络
    torch.save(net.state_dict(), 'net_params.pkl')   # 只保存网络中的参数 (速度快, 占内存少)
    print('save_done')


#提取网络
def restore_net(meet):
    # restore entire net1 to net2
    meet = torch.load('net.pkl')
    torch.save(meet.state_dict(), 'net_params.pkl')  # 只保存网络中的参数 (速度快, 占内存少)
    return meet


#提取网络
def restore_params():
    # 新建 net3
    net2 = mobilenetv2.mobilenetv2(num_classes=2)
    # 将保存的参数复制到 net3
    net2.load_state_dict(torch.load('net_params.pkl'))
    return net2


#尝试搭建新的网络
class CNNnew(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential(  # (1, 28, 28)
            nn.Conv2d(
                in_channels=1, # 输入通道数，若图片为RGB则为3通道
                out_channels=1, # 输出通道数，即多少个卷积核一起卷积
                kernel_size=5, # 卷积核大小
                stride=1, # 卷积核移动步长
                padding=2, # 边缘增加的像素，使得得到的图片长宽没有变化
            ),# (1, 28, 28)，点卷积
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 32, 3, 1, 1), # (32, 28, 28)
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2), # 池化 (32, 14, 14)
        )
        self.conv3 = nn.Sequential(# (32, 14, 14)
            nn.Conv2d(32, 64, 3, 1, 1),# (64, 14, 14)
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
        )
        self.conv4 = nn.Sequential(
            nn.Conv2d(64, 64, 3, 1, 1),# (64, 14, 14)
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),# (64, 7, 7)
        )
        self.out = nn.Sequential(
            nn.Dropout(p = 0.5), # 抑制过拟合
            nn.Linear(64 * 7 * 7, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(p = 0.5),
            nn.Linear(512, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(p = 0.5),
            nn.Linear(512, 10),
        )
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = x.view(x.size(0), -1) # (batch_size, 64*7*7)
        output = self.out(x)
        return output


def dog_cat_data():
    data_transform = transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])

    dog_cat_train_dataset = datasets.ImageFolder(root=r'C:\Users\Yuki\Desktop\bugs\python\graduation_design\dog&cat', transform=data_transform)
    dog_cat_train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=4, shuffle=True, num_workers=4)

    dog_cat_test_dataset = datasets.ImageFolder(root='test/', transform=data_transform)
    dog_cat_test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=4, shuffle=True, num_workers=4)
    return dog_cat_train_loader,dog_cat_test_loader


def datatransform():
    data_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return data_transform


transform = transforms.Compose([transforms.Resize(256),
                                transforms.CenterCrop(224),
                                transforms.ToTensor(),
                                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

# data_image = {x:datasets.ImageFolder(root = r"C:\Users\Yuki\Desktop\bugs\python\graduation_design\dog&cat",
#                                      transform = transform)
#               for x in ["train", "val"]}
#
# data_loader_image = {x:torch.utils.data.DataLoader(dataset=data_image[x],
#                                                 batch_size = 4,
#                                                 shuffle = True)
#                      for x in ["train", "val"]}
# classes = data_image["train"].classes
# classes_index = data_image["train"].class_to_idx
# print(classes)
# print(classes_index)
# print(len(data_image["train"]))
# print(len(data_image["val"]))
