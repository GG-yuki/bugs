import torch.nn as nn
from torch.nn import init
import torch

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
*    mobilenetv1
*
* 返 回 值：softmax,2个概率值，用来预测猫狗
*
* 抛出异常：
*
* 作  者：qiwei_ji 2020/5/31
*
* 网络结构：
*
*       mobilenetv1(
*          (conv1): Sequential(
*           (0): Conv2d(1, 1, kernel_size=(5, 5), stride=(1, 1), padding=(2, 2))
*           (1): BatchNorm2d(1, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
*            (2): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
*            (3): ReLU()
*          )
*          (conv2): Sequential(
*            (0): Conv2d(1, 32, kernel_size=(1, 1), stride=(1, 1))
*            (1): BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
*            (2): ReLU()
*            (3): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
*          )
*         (out): Linear(in_features=1568, out_features=10, bias=True)
*        )
* ============================================================*/
'''
#
#
# class classifier(torch.nn.Module):
#     def __init__(self, in_channels, num_classes):
#         super().__init__()
#         self.conv = torch.nn.Conv2d(
#             in_channels=in_channels,
#             out_channels=num_classes,
#             kernel_size=1,
#             bias=True)
#
#     def forward(self, x):
#         x = self.conv(x)
#         x = x.view(x.size(0), -1)
#         return x
#
#     def init_params(self):
#         torch.nn.init.xavier_normal_(self.conv.weight, gain=1.0)


class MobileNetV1(nn.Module):
    def __init__(self, num_classes, sobel):
        super(MobileNetV1, self).__init__()

        def conv_bn(inp, oup, stride):
            return nn.Sequential(
                nn.Conv2d(inp, oup, 3, stride, 1, bias=False),
                nn.BatchNorm2d(oup),
                nn.ReLU(inplace=True)
            )

        def conv_dw(inp, oup, stride):
            return nn.Sequential(
                nn.Conv2d(inp, inp, 3, stride, 1, groups=inp, bias=False),
                nn.BatchNorm2d(inp),
                nn.ReLU(inplace=True),

                nn.Conv2d(inp, oup, 1, 1, 0, bias=False),
                nn.BatchNorm2d(oup),
                nn.ReLU(inplace=True),
            )

        if sobel:
            grayscale = nn.Conv2d(3, 1, kernel_size=1, stride=1, padding=0)
            grayscale.weight.data.fill_(1.0 / 3.0)
            grayscale.bias.data.zero_()
            sobel_filter = nn.Conv2d(1, 2, kernel_size=3, stride=1, padding=1)
            sobel_filter.weight.data[0, 0].copy_(
                torch.FloatTensor([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
            )
            sobel_filter.weight.data[1, 0].copy_(
                torch.FloatTensor([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
            )
            sobel_filter.bias.data.zero_()
            self.sobel = nn.Sequential(grayscale, sobel_filter)
            for p in self.sobel.parameters():
                p.requires_grad = False
        else:
            self.sobel = None
        self.classifier = nn.Sequential(
            nn.Linear(1024, 1000),
            nn.ReLU(True),
        )
        self.features = nn.Sequential(
            conv_bn(2, 32, 1),
            # conv_bn(3, 32, 1),
            conv_dw(32, 64, 1),
            conv_dw(64, 128, 1),
            conv_dw(128, 128, 1),
            conv_dw(128, 256, 2),
            conv_dw(256, 256, 1),
            conv_dw(256, 512, 2),
            conv_dw(512, 512, 1),
            conv_dw(512, 512, 1),
            conv_dw(512, 512, 1),
            conv_dw(512, 512, 1),
            conv_dw(512, 512, 1),
            conv_dw(512, 1024, 2),
            conv_dw(1024, 1024, 1),
        )
        self.avg = nn.AdaptiveAvgPool2d(1)
        self.top_layer = nn.Linear(1000, num_classes)
        self.init_params()

    def forward(self, x):
        if self.sobel:
            x = self.sobel(x)
        x = self.features(x)
        x = self.avg(x)
        # print(x.size())
        x = x.view(x.size(0), -1)
        # print(x.size())
        x = self.classifier(x)
        # print(x.size())
        # print(x.size(0))
        if self.top_layer:
            x = self.top_layer(x)
        return x

    def init_params(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                init.kaiming_normal_(m.weight, mode='fan_out')
                if m.bias is not None:
                    init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                init.constant_(m.weight, 1)
                init.constant_(m.bias, 0)


# def test():
#     net = MobileNetV1(100, True)
#     x = torch.randn(2, 3, 32, 32)
#     y = net(x)
#     print(y.size())
#
#
# test()
