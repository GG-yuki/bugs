# coding=utf-8
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
from support import *
# from mobilenetv1 import *
from mobilenetv1_att import *
from mobilenetv2 import *
from mobilenetv2_att import *
from mobilenetv3 import *
from mobilenetv3_att import *
from shufflenetv1 import *

# 部分训练参数参数
data_root = './dataset'
epochs = 100  # 训练次数
batch_size = 64  # 批处理大小
num_workers = 4  # 多线程
LR = 0.04  # 初始学习速率
weight_decay = 1e-4

# seed
seed: Optional[int] = 31

# 对加载的图像作归一化处理，并裁剪为[224x224x3]大小的图像，加载数据
load_data = Data_loader(data_root, num_workers, batch_size)
train_loader = load_data.trainloader()
test_loader = load_data.testloader()

# 网络实例化
# net = restore_params() 加载之前存储的网络参数
net = MobileNetV1(100).cuda()  # 分类
# net = MobileNetV2(100).cuda()  # 分类
# net = MobileNetV3_Large_CBAM(100).cuda()  # 分类
# net = ShuffleNetV1().cuda()
result = train(net, epochs, LR, train_loader, test_loader, weight_decay=weight_decay)
write_result(format(net.__class__.__name__), epochs, batch_size, num_workers, LR, result[0], weight_decay, result[1],
             result[2])

print("mobilenetv3 large cbam cifar100")
