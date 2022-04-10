import torch.nn as nn
import torch
import torch.nn.functional as F

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


class MobileNetV1(nn.Module):
    def __init__(self, num_classes):
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

        self.model = nn.Sequential(
            conv_bn(3, 32, 2),
            conv_dw(32, 64, 1),
            conv_dw(64, 128, 2),
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
            nn.AvgPool2d(7),
        )
        self.fc1 = nn.Linear(1024, 1000)
        self.fc2 = nn.Linear(1000, num_classes)

    def forward(self, x):
        x = self.model(x)
        x = x.view(-1, 1024)
        x = self.fc1(x)
        x = self.fc2(x)
        output = F.softmax(x, dim=1)  # import torch.nn.funtional as F
        return output


def test():
    net = MobileNetV1(2)
    x = torch.randn(2, 3, 224, 224)
    y = net(x)
    print(y)


test()
