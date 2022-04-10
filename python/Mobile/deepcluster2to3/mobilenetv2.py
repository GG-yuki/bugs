'''
/*============================================================
*
* 函 数 名：mobilenetv1()
*
* 参  数：
*
*    tensor,4维，m样本*n通道*尺寸*尺寸
*
* 功能描述:
*
*    mobilenetv2
*
* 返 回 值：softmax,10个概率值
*
* 抛出异常：
*
* 作  者：qiwei_ji 2020/3/19
* ============================================================*/
'''
# coding:utf-8
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import init

class Head(nn.Module):  # MobileNet_2 网络的第1层
    def __init__(self):
        super(Head, self).__init__()
        self.conv = nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1, bias=False)
        self.bn = nn.BatchNorm2d(32)

    def forward(self, x):
        out = F.relu6(self.bn(self.conv(x)))
        return out


class Tail(nn.Module):  # MobileNet_2 网络的最后3层
    def __init__(self):
        super(Tail, self).__init__()
        self.conv_1280 = nn.Conv2d(320, 1280, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn_1280 = nn.BatchNorm2d(1280)
        self.conv_end = nn.Conv2d(1280, 1000, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn_end = nn.BatchNorm2d(1000)

    def forward(self, x):
        out = F.relu6(self.bn_1280(self.conv_1280(x)))
        out = F.avg_pool2d(out, kernel_size=7)
        # out = F.relu6(self.bn_end(self.conv_end(out))) # 这里不能这么写，因为当某个通道只有1个值时，使用batchnorm会导致输出结果为0
        out = self.conv_end(out)
        return out


class Bottleneck(nn.Module):  # MobileNet_2 网络的Bottleneck层
    n = 0

    def __init__(self, in_planes, expansion, out_planes, repeat_times, stride):
        super(Bottleneck, self).__init__()
        inner_channels = in_planes * expansion
        # Bottlencek3个组件之一:'1*1-conv2d'
        self.conv1 = nn.Conv2d(in_planes, inner_channels, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn1 = nn.BatchNorm2d(inner_channels)
        # Bottlencek3个组件之二:dwise
        self.conv2_with_stride = nn.Conv2d(inner_channels, inner_channels, kernel_size=3, stride=stride, padding=1,
                                           groups=inner_channels, bias=False)  # layer==1 stride=s
        self.conv2_no_stride = nn.Conv2d(inner_channels, inner_channels, kernel_size=3, stride=1, padding=1,
                                         groups=inner_channels, bias=False)  # layer>1  stride=1
        # Bottlencek3个组件之三:linear-1*1-conv2d'
        self.conv3 = nn.Conv2d(inner_channels, out_planes, kernel_size=1, stride=1, padding=0, groups=1, bias=False)
        # 当某个bottleneck重复出现时，'1*1-conv2d'的输入输出的通道数发生变化，不能再使用conv1了
        self.conv_inner = nn.Conv2d(out_planes, expansion * out_planes, kernel_size=1, stride=1, padding=0, bias=False)
        # 当某个bottleneck重复出现时，dwise的输入输出的通道数发生变化，不能再使用conv2_with_stride和conv2_no_stride了
        self.conv_inner_with_stride = nn.Conv2d(expansion * out_planes, expansion * out_planes, kernel_size=3,
                                                stride=stride, padding=1, groups=out_planes,
                                                bias=False)  # layer==1 stride=s
        self.conv_inner_no_stride = nn.Conv2d(expansion * out_planes, expansion * out_planes, kernel_size=3, stride=1,
                                              padding=1, groups=out_planes, bias=False)  # layer>1  stride=1
        # 当某个bottleneck重复出现时，'linear-1*1-conv2d'的输入输出的通道数发生变化，不能再使用了
        self.conv3_inner = nn.Conv2d(expansion * out_planes, out_planes, kernel_size=1, stride=1, padding=0, groups=1,
                                     bias=False)
        # 当某个bottleneck重复出现时，batchnorm的通道数也同样发生了变化
        self.bn_inner = nn.BatchNorm2d(expansion * out_planes)
        self.bn2 = nn.BatchNorm2d(out_planes)
        self.n = repeat_times

    def forward(self, x):
        out = F.relu6(self.bn1(self.conv1(x)))
        out = F.relu6(self.bn1(self.conv2_with_stride(out)))
        out = self.conv3(out)
        out = self.bn2(out)
        count = 2
        while (count <= self.n):
            temp = out
            out = F.relu6(self.bn_inner(self.conv_inner(out)))
            out = F.relu6(self.bn_inner(self.conv_inner_no_stride(out)))
            out = self.conv3_inner(out)
            out = self.bn2(out)
            out = out + temp
            count = count + 1
        return out


class MobileNetV2(nn.Module):  # MobileNet_2网络的完整定义
    # [input_channels, t, c, n, s] 论文中的参数列表
    param = [[32, 1, 16, 1, 1],
             [16, 6, 24, 2, 2],
             [24, 6, 32, 3, 2],
             [32, 6, 64, 4, 2],
             [64, 6, 96, 3, 1],
             [96, 6, 160, 3, 2],
             [160, 6, 320, 1, 1]]

    def __init__(self ,num):
        super(MobileNetV2, self).__init__()
        self.layers = self._make_layers()
        self.fc1 = nn.Linear(1000, 10)
        self.fc2 = nn.Linear(10, num)

    def _make_layers(self):
        layer = []
        layer.append(Head())
        for i in range(len(self.param)):
            layer.append(
                Bottleneck(self.param[i][0], self.param[i][1], self.param[i][2], self.param[i][3], self.param[i][4]))
        layer.append(Tail())
        return nn.Sequential(*layer)

    def forward(self, x):
        out = self.layers(x)
        out = out.view(-1, 1000)
        out = self.fc1(out)
        out = self.fc2(out)
        out = F.softmax(out, dim=1)
        return out

    def init_params(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                init.kaiming_normal_(m.weight, mode='fan_out')
                if m.bias is not None:
                    init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                init.constant_(m.weight, 1)
                init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                init.normal_(m.weight, std=0.001)
                if m.bias is not None:
                    init.constant_(m.bias, 0)


# def test():
#     net = MobileNet2(1000)  # 输出的类别数目
#     x = torch.randn(1, 3, 224, 224)  # 个数,通道数,宽,高
#     y = net(x)
#     print(y.size())
#
#
# test()
net = MobileNetV2(2)
x = torch.randn(2, 3, 224, 224)
y = net(x)
print(y)

# start build CNN
# class Block(nn.Module):
#     '''expand + depthwise + pointwise'''
#     def __init__(self, in_planes, out_planes, expansion, stride):
#         super(Block, self).__init__()
#         self.stride = stride
#
#         planes = expansion * in_planes
#         self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1,
#                                stride=1, padding=0, bias=False)
#         self.bn1 = nn.BatchNorm2d(planes)
#         self.conv2 = nn.Conv2d(planes, planes, kernel_size=3,
#                                stride=stride, padding=1, groups=planes,
#                                bias=False)
#         self.bn2 = nn.BatchNorm2d(planes)
#         self.conv3 = nn.Conv2d(planes, out_planes, kernel_size=1,
#                                stride=1, padding=0, bias=False)
#         self.bn3 = nn.BatchNorm2d(out_planes)
#
#         self.shortcut = nn.Sequential()
#         if stride == 1 and in_planes != out_planes:
#             self.shortcut = nn.Sequential(
#                 nn.Conv2d(in_planes, out_planes, kernel_size=1,
#                           stride=1, padding=0, bias=False),
#                 nn.BatchNorm2d(out_planes),
#             )
#
#     def forward(self, x):
#         out = F.relu(self.bn1(self.conv1(x)))
#         out = F.relu(self.bn2(self.conv2(out)))
#         out = self.bn3(self.conv3(out))
#         out = out + self.shortcut(x) if self.stride==1 else out
#         return out
#
#
# class mobilenetv2(nn.Module):
#     # (expansion, out_planes, num_blocks, stride)
#     cfg = [(1,  16, 1, 1),
#            (6,  24, 2, 1),  # NOTE: change stride 2 -> 1 for CIFAR10
#            (6,  32, 3, 2),
#            (6,  64, 4, 2),
#            (6,  96, 3, 1),
#            (6, 160, 3, 2),
#            (6, 320, 1, 1)]
#
#     def __init__(self):
#         super(mobilenetv2, self).__init__()
#         # NOTE: change conv1 stride 2 -> 1 for CIFAR10
#         self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1,
#                                padding=1, bias=False)
#         self.bn1 = nn.BatchNorm2d(32)
#         self.layers = self._make_layers(in_planes=32)
#         self.conv2 = nn.Conv2d(320, 1280, kernel_size=1, stride=1,
#                                padding=0, bias=False)
#         self.bn2 = nn.BatchNorm2d(1280)
#         self.linear = nn.Linear(1280,1000)
#         self.fc1 = nn.Linear(1000, 10)
#         self.fc2 = nn.Linear(10, 2)
#     def _make_layers(self, in_planes):
#         layers = []
#         for expansion, out_planes, num_blocks, stride in self.cfg:
#             strides = [stride] + [1]*(num_blocks-1)
#             for stride in strides:
#                 layers.append(
#                     Block(in_planes, out_planes, expansion, stride))
#                 in_planes = out_planes
#         return nn.Sequential(*layers)
#
#     def forward(self, x):
#         out = F.relu(self.bn1(self.conv1(x)))
#         out = self.layers(out)
#         out = F.relu(self.bn2(self.conv2(out)))
#         # NOTE: change pooling kernel_size 7 -> 4 for CIFAR10
#         out = F.avg_pool2d(out, 4)
#         out = out.view(-1,1280)
#         out = self.linear(out)
#         out = self.fc1(out)
#         out = self.fc2(out)
#         out = F.softmax(out, dim=1)  # import torch.nn.funtional as F
#         return out

#model.py

# from torch import nn
# import torch
#
#
# def _make_divisible(ch, divisor=8, min_ch=None):
#     """
#     This function is taken from the original tf repo.
#     It ensures that all layers have a channel number that is divisible by 8
#     It can be seen here:
#     https://github.com/tensorflow/models/blob/master/research/slim/nets/mobilenet/mobilenet.py
#     """
#     if min_ch is None:
#         min_ch = divisor
#     new_ch = max(min_ch, int(ch + divisor / 2) // divisor * divisor)
#     # Make sure that round down does not go down by more than 10%.
#     if new_ch < 0.9 * ch:
#         new_ch += divisor
#     return new_ch
#
#
# class ConvBNReLU(nn.Sequential):
#     def __init__(self, in_channel, out_channel, kernel_size=3, stride=1, groups=1):#groups=1普通卷积
#         padding = (kernel_size - 1) // 2
#         super(ConvBNReLU, self).__init__(
#             nn.Conv2d(in_channel, out_channel, kernel_size, stride, padding, groups=groups, bias=False),
#             nn.BatchNorm2d(out_channel),
#             nn.ReLU6(inplace=True)
#         )
#
# #到残差结构
# class InvertedResidual(nn.Module):
#     def __init__(self, in_channel, out_channel, stride, expand_ratio):#expand_ratio扩展因子
#         super(InvertedResidual, self).__init__()
#         hidden_channel = in_channel * expand_ratio
#         self.use_shortcut = stride == 1 and in_channel == out_channel
#
#         layers = []
#         if expand_ratio != 1:
#             # 1x1 pointwise conv
#             layers.append(ConvBNReLU(in_channel, hidden_channel, kernel_size=1))
#         layers.extend([
#             # 3x3 depthwise conv
#             ConvBNReLU(hidden_channel, hidden_channel, stride=stride, groups=hidden_channel),
#             # 1x1 pointwise conv(linear)
#             nn.Conv2d(hidden_channel, out_channel, kernel_size=1, bias=False),
#             nn.BatchNorm2d(out_channel),
#         ])
#
#         self.conv = nn.Sequential(*layers)
#
#     def forward(self, x):
#         if self.use_shortcut:
#             return x + self.conv(x)
#         else:
#             return self.conv(x)
#
#
# class mobilenetv2(nn.Module):
#     def __init__(self, num_classes=2, alpha=1.0, round_nearest=8):#alpha超参数
#         super(mobilenetv2, self).__init__()
#         block = InvertedResidual
#         input_channel = _make_divisible(32 * alpha, round_nearest)
#         last_channel = _make_divisible(1280 * alpha, round_nearest)
#
#         inverted_residual_setting = [
#             # t, c, n, s
#             [1, 16, 1, 1],
#             [6, 24, 2, 2],
#             [6, 32, 3, 2],
#             [6, 64, 4, 2],
#             [6, 96, 3, 1],
#             [6, 160, 3, 2],
#             [6, 320, 1, 1],
#         ]
#
#         features = []
#         # conv1 layer
#         features.append(ConvBNReLU(3, input_channel, stride=2))
#         # building inverted residual residual blockes
#         for t, c, n, s in inverted_residual_setting:
#             output_channel = _make_divisible(c * alpha, round_nearest)
#             for i in range(n):
#                 stride = s if i == 0 else 1
#                 features.append(block(input_channel, output_channel, stride, expand_ratio=t))
#                 input_channel = output_channel
#         # building last several layers
#         features.append(ConvBNReLU(input_channel, last_channel, 1))
#         # combine feature layers
#         self.features = nn.Sequential(*features)
#
#         # building classifier
#         self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
#         self.classifier = nn.Sequential(
#             nn.Dropout(0.2),
#             nn.Linear(last_channel, num_classes)
#         )
#
#         # weight initialization
#         for m in self.modules():
#             if isinstance(m, nn.Conv2d):
#                 nn.init.kaiming_normal_(m.weight, mode='fan_out')
#                 if m.bias is not None:
#                     nn.init.zeros_(m.bias)
#             elif isinstance(m, nn.BatchNorm2d):
#                 nn.init.ones_(m.weight)
#                 nn.init.zeros_(m.bias)
#             elif isinstance(m, nn.Linear):
#                 nn.init.normal_(m.weight, 0, 0.01)
#                 nn.init.zeros_(m.bias)
#
#     def forward(self, x):
#         x = self.features(x)
#         x = self.avgpool(x)
#         x = torch.flatten(x, 1)
#         x = self.classifier(x)
#         x = F.softmax(x,dim=1)
#         return x