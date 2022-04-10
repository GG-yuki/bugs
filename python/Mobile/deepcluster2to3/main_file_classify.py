"""
/********************************************************************
*
*  文件名：main_file_classify.py
*
*  文件描述：猫狗识别
*
*  创建人： qiwei_ji, 2020年10月4日
*
*  版本号：1.2_alpha
*
*  修改记录：10
*
************************* *******************************************/
"""
# coding=utf-8
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
from support_for_classify import *
# from mobilenetv1 import *
# from mobilenetv2 import *
# from mobilenetv3 import *
# from v3_pam import *
from mobilenetv1_sobel import *
# from mobilenetv1_no_sobel import *

# 部分训练参数参数
# data_root = './dataset'
epochs = 200  # 训练次数
batch_size = 128  # 批处理大小
num_workers = 4  # 多线程
LR = 0.04  # 初始学习速率
weight_decay = 1e-4

# seed
torch.manual_seed(31)
torch.cuda.manual_seed_all(31)
np.random.seed(31)

# 对加载的图像作归一化处理，并裁剪为[224x224x3]大小的图像，加载数据
load_data = Data_loader(num_workers, batch_size)
train_loader = load_data.trainloader()
test_loader = load_data.testloader()

# 网络实例化
# net = restore_params() 加载之前存储的网络参数
# net = MobileNetV1(100).cuda()  # 分类
# net = MobileNetV2(100).cuda()  # 分类
# net = MobileNetV3_Small_PAM(100).cuda()  # 分类
# net = MobileNetV1(num_classes=100, sobel=True)
# model = MobileNetV1(100).cuda()
net = load_model()
# model.cuda()
# cudnn.benchmark = True
#
# # freeze the features layers
for param in net.features.parameters():
    param.requires_grad = False
net.classifier = Classifier(1024, 100)
net.top_layer = None
net = net.cuda()

result = train(net, epochs, LR, train_loader, test_loader, weight_decay=weight_decay)
write_result(format(net.__class__.__name__), epochs, batch_size, num_workers, LR, result[0], weight_decay, result[1],
             result[2])
