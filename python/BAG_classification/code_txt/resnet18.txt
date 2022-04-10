# -*- coding: utf-8 -*-
'''
/********************************************************************
*
*  文件名：main.py
*
*  文件描述：boy & girl classification
*
*  创建人： qiwei_ji, 2020年11月23日
*
*  版本号：2.0
*
*  修改记录：2
*
********************************************************************/
'''

from support import *
from torchvision import datasets
import argparse


parser = argparse.ArgumentParser(description='construct your own neural network')
parser.add_argument('--learningrate',type=float,default=0.001, help='define learning rate')
parser.add_argument('--epochs',type=int,default=40, help='define training epochs',)
parser.add_argument('--num_workers',type=int,default=0, help='define the number of thread',)
parser.add_argument('--batch_size',type=int,default=1, help='define the batch size',)
parser.add_argument('--train_folder', type=str, default='./dataset/train', help='define your train loader')
parser.add_argument('--test_folder', type=str, default='./classmate_photo/', help='define your test loader')
args = parser.parse_args()


# 对加载的图像作归一化处理， 并裁剪为[224x224x3]大小的图像
data_transform = datatransform()


# 加载数据,train和test路径下分文件夹归放训练和测试数据，此处需自行修改,文件夹存储方式如下所示
# ├── train
# │   ├── 1.jpg
# │   ├── 2.jpg
# │   ├── 3.jpg
train_dataset = datasets.ImageFolder(root=args.train_folder,
                                     transform=data_transform)
train_loader = torch.utils.data.DataLoader(train_dataset,
                                           batch_size=args.batch_size,
                                           shuffle=True,
                                           num_workers=args.num_workers)


test_dataset = datasets.ImageFolder(root=args.test_folder,
                                    transform=data_transform)
test_loader = torch.utils.data.DataLoader(test_dataset,
                                          batch_size=args.batch_size,
                                          shuffle=True,
                                          num_workers=args.num_workers)


# # 网络实例化
# net = loadmodel(num_classes=2)
# # 训练和测试
# train(net,epochs,learningrate,train_loader,test_loader)
# # 保存网络
# save_18(net)


# 提取网络并测试，注意这部分代码和前面并不兼容
net = restore_18()
test(net,test_loader)
