import torch
import torch.nn as nn
import torch.nn.functional as F


'''
/*============================================================
*
* 函 数 名：mobilenetv1_block_test()
*
* 参  数：
*
*    tensor,4维，m样本*n通道*尺寸*尺寸
*
* 功能描述:
*
*    mobilenetv1中的点卷积，没什么用
*
* 返 回 值：softmax,10个概率值
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
# start build CNN
class mobilenetv1_block_test(nn.Module):
    def __init__(self):
        super(mobilenetv1, self).__init__()
        # 一个卷积层
        self.conv1 = nn.Sequential(
            nn.Conv2d(  # (1,28,28)
                in_channels=1,      # 1个通道
                out_channels=1,    # 输出多少层 也就是有多少个过滤器
                kernel_size=5,      # 过滤器的大小
                stride=1,           # 步长
                padding=2           # 填白
            ),      # --> (1,28,28)
            nn.BatchNorm2d(1),      # -->(1,28,28)
            nn.MaxPool2d(kernel_size=2),      # -->(1,14,14)
            nn.ReLU(),      # -->(1,14,14)
        )
        self.conv2 = nn.Sequential(     # --> (1,14,14)
            nn.Conv2d(1,32,1,1,0), # (32,14,14)
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2) # --> (32,7,7)
        )
        self.out = nn.Linear(32*7*7,10) # 将三维的数据展为2维的数据
    def forward(self,x):
        x = self.conv1(x)
        x = self.conv2(x)       # (batch,64,7,7)
        x = x.view(x.size(0), -1)
        output = F.softmax(self.out(x),dim=1)    # import torch.nn.funtional as F
        return output
#
# cnn = mobilenetv1()
# print(cnn)  # net architecture


# class Net(nn.Module):
#     def __init__(self):
#         super(Net, self).__init__()
#
#         self.conv1 = nn.Conv2d(3, 6, 5)
#         self.pool = nn.MaxPool2d(2, 2)
#         self.conv2 = nn.Conv2d(6, 16, 5)
#         self.fc1 = nn.Linear(16 * 18 * 18, 800)
#         self.fc2 = nn.Linear(800, 120)
#         self.fc3 = nn.Linear(120, 2)
#
#     def forward(self, x):
#         x = self.pool(F.relu(self.conv1(x)))
#         x = self.pool(F.relu(self.conv2(x)))
#         x = x.view(-1, 16 * 18 * 18)
#         x = F.relu(self.fc1(x))
#         x = F.relu(self.fc2(x))
#         x = self.fc3(x)
#         return x


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
class mobilenetv1(nn.Module):
    def __init__(self):
        super(mobilenetv1, self).__init__()

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
        self.fc2 = nn.Linear(1000, 10)
        self.fc3 = nn.Linear(10, 2)

    def forward(self, x):
        x = self.model(x)
        x = x.view(-1, 1024)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        output = F.softmax(x, dim=1)  # import torch.nn.funtional as F
        return output


# def test():
#     net = mobilenetv1()
#     x = torch.randn(2,3,224,224)
#     y = net(x)
#     print(y.size())
# test()
net = mobilenetv1()
print(net)

