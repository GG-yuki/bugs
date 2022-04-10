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

# 调用另一个网络，并加载先前网络的参数
model_18_front = front_resnet18().cuda()
model_18_later = later_resnet18().cuda()

model_18_front.load_state_dict(torch.load(r'./pkl/ResNet/epoch_149_net_params.pkl'), strict=False)
model_18_later.load_state_dict(torch.load(r'./pkl/ResNet/epoch_149_net_params.pkl'), strict=False)
