"""
/********************************************************************
*
*  文件名：main.py
*
*  文件描述：分类
*
*  创建人： qiwei_ji, 2021年7月15日
*
*  版本号：1.0_alpha
*
*  修改记录：1
*
************************* *******************************************/
"""
# coding=utf-8
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
from support import *
from resnet import resnet18, resnet34
from apart_network import *
from data_loader import Data_loader_self

# 部分训练参数参数
data_root = './dataset'
epochs = 200  # 训练次数
batch_size = 32  # 批处理大小
num_workers = 4  # 多线程
LR = 0.04  # 初始学习速率
weight_decay = 1e-4

# seed
set_random_seed(31)

# 对加载的图像作归一化处理，并裁剪为[224x224x3]大小的图像，加载数据
load_data = Data_loader_self(data_root, num_workers, batch_size)
train_loader = load_data.trainloader()
test_loader = load_data.testloader()

# 网络实例化
net = resnet18(num_classes=100).cuda()  #
net.load_state_dict(torch.load(r'./pkl/ResNet/epoch_149_net_params.pkl'), strict=False)
select_sample(net, train_loader)
