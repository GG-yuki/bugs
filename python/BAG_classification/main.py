# -*- coding: utf-8 -*-
'''
/********************************************************************
*
*  文件名：main.py
*
*  文件描述：boy & girl classification
*
*  创建人： qiwei_ji, 2020年11月20日
*
*  版本号：1.0
*
*  修改记录：1
*
********************************************************************/
'''

from support import *
from torchvision import datasets


learningrate = 0.001 # 初始学习速率，学习过程LR会发生改变，具体变化可参照support文件最后一行
epochs = 100 # 训练轮数
num_workers = 0 # 多线程
batch_size = 1  # 批处理大小


# 对加载的图像作归一化处理， 并裁剪为[224x224x3]大小的图像
data_transform = datatransform()


# 加载数据,train和test路径下分文件夹归放训练和测试数据，此处需自行修改,文件夹存储方式如下所示
# ├── train
# │   ├── 1.jpg
# │   ├── 2.jpg
# │   ├── 3.jpg
train_dataset = datasets.ImageFolder(root=r'/home/jijl/My_project/BAG_classification/dataset/train',
                                     transform=data_transform)
train_loader = torch.utils.data.DataLoader(train_dataset,
                                           batch_size=batch_size,
                                           shuffle=True,
                                           num_workers=num_workers)

test_dataset = datasets.ImageFolder(root=r'/home/jijl/My_project/BAG_classification/dataset/test',
                                    transform=data_transform)
test_loader = torch.utils.data.DataLoader(test_dataset,
                                          batch_size=batch_size,
                                          shuffle=True,
                                          num_workers=num_workers)


# 网络实例化
net = loadmodel(num_classes=2)
# 训练
train(net,epochs,learningrate,train_loader,test_loader)