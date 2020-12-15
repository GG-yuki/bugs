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
********************************************************************/
"""
# coding=utf-8
from support import *
from mobilenetv1 import *
# from mobilenetv2 import *
# from mobilenetv3 import *
from torchvision import datasets

# 部分训练参数参数
epochs = 200  # 训练次数
batch_size = 128  # 批处理大小
num_workers = 4  # 多线程
LR = 0.001  # 初始学习速率

# seed
seed: Optional[int] = None

# 对加载的图像作归一化处理， 并裁剪为[224x224x3]大小的图像
data_transform = datatransform()
test_transform = transform_test()

print(torch.cuda.is_available())
# 加载数据,train和test路径下分文件夹归放数据
train_dataset = datasets.CIFAR10(root='./data', train=True, download=False, transform=data_transform)
train_loader = torch.utils.data.DataLoader(train_dataset,
                                           batch_size=batch_size,
                                           shuffle=True,
                                           num_workers=num_workers)

test_dataset = datasets.CIFAR10(root='./data', train=False, download=False, transform=test_transform)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)

# 网络实例化
# net = restore_params() 加载之前存储的网络参数
# net = MobileNetV1(num_classes=10).cuda()  # 分类
net = load_net('epoch_299')
# net = loadmodel(10)  # 分类
# net = net.cuda()
# net = MobileNetV3_Small(10).cuda() # 分类
train(net, epochs, LR, train_loader, test_loader)
