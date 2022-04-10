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
batch_size = 128  # 批处理大小
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
net = resnet18(num_classes=100).cuda()  # 分类
result1 = train(net, epochs, LR, train_loader, test_loader, model_name='resnet18', weight_decay=weight_decay)
write_result(format(net.__class__.__name__), epochs, batch_size, num_workers, LR, result1[0], weight_decay, result1[1],
             result1[2])

net2 = resnet34(num_classes=100).cuda()  # 分类
result2 = train(net2, epochs, LR, train_loader, test_loader, model_name='resnet34', weight_decay=weight_decay)
write_result(format(net2.__class__.__name__), epochs, batch_size, num_workers, LR, result2[0], weight_decay, result2[1],
             result2[2])

# 调用另一个网络，并加载先前网络的参数
model_18_front = front_resnet18().cuda()
model_18_later = later_resnet18().cuda()
model_34_front = front_resnet34().cuda()
model_34_later = later_resnet34().cuda()

model_18_front.load_state_dict(torch.load(r'./pkl/ResNet/epoch_149_net_params.pkl'), strict=False)
model_18_later.load_state_dict(torch.load(r'./pkl/ResNet/epoch_149_net_params.pkl'), strict=False)

result = train_apart(model_18_front, model_34_front, model_18_later, model_34_later, epochs, LR, train_loader, test_loader, model_name1='model_34_front', model_name2='model_34_later', weight_decay=weight_decay)
write_result(format(net.__class__.__name__), epochs, batch_size, num_workers, LR, result1[0], weight_decay, result1[1],
             result1[2])
