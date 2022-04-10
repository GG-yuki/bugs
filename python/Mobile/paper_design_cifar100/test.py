import torch.nn as nn
from torch.nn import init
import torch
import torch.nn.functional as F


# class SeModule(nn.Module):  # 第二种
#     def __init__(self, channel, reduction=16):
#         super(SeModule, self).__init__()
#         self.avg_pool = nn.AdaptiveAvgPool2d(1)
#         self.fc = nn.Sequential(
#             nn.Linear(channel, channel // reduction, bias=False),
#             nn.ReLU(inplace=True),
#             nn.Linear(channel // reduction, channel, bias=False),
#             nn.Sigmoid()
#         )
#
#     def forward(self, x):
#         b, c, _, _ = x.size()
#         y = self.avg_pool(x).view(b, c)
#         y = self.fc(y).view(b, c, 1, 1)
#         return x * y.expand_as(x)


class ChannelAttentionModule(nn.Module):
    def __init__(self, channel, ratio=4):
        super(ChannelAttentionModule, self).__init__()
        # 使用自适应池化缩减map的大小，保持通道不变
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)

        self.shared_MLP = nn.Sequential(
            nn.Conv2d(channel, channel // ratio, 1, bias=False),
            nn.ReLU(),
            nn.Conv2d(channel // ratio, channel, 1, bias=False)
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # avgout = self.shared_MLP(self.avg_pool(x))
        # maxout = self.shared_MLP(self.max_pool(x))
        out = self.shared_MLP(self.avg_pool(x) + self.max_pool(x))
        return self.sigmoid(out)


class SpatialAttentionModule(nn.Module):
    def __init__(self, channel):
        super(SpatialAttentionModule, self).__init__()
        self.conv2d = nn.Conv2d(in_channels=channel, out_channels=1, kernel_size=5, stride=1, padding=2)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # map尺寸不变，缩减通道
        avgout = torch.mean(x, dim=1, keepdim=True)
        maxout, _ = torch.max(x, dim=1, keepdim=True)
        # out = torch.cat([avgout, maxout], dim=1)
        # out = self.sigmoid(self.conv2d(out))
        out = self.sigmoid(self.conv2d(maxout + avgout))
        return out


class SpatialAttentionModule2(nn.Module):
    def __init__(self):
        super(SpatialAttentionModule2, self).__init__()
        self.conv2d = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=5, stride=1, padding=2)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # map尺寸不变，缩减通道
        avgout = torch.mean(x, dim=1, keepdim=True)
        maxout, _ = torch.max(x, dim=1, keepdim=True)
        out = avgout + maxout
        out = self.sigmoid(self.conv2d(out))
        return out


class SeModule(nn.Module):
    def __init__(self, channel):
        super(SeModule, self).__init__()
        self.channel_attention = ChannelAttentionModule(channel)
        self.spatial_attention = SpatialAttentionModule(channel)

    def forward(self, x):
        out1 = self.channel_attention(x) * x
        out2 = self.spatial_attention(x) * x
        return (out1 + out2 + x)


class SpatialAttentionModule3(nn.Module):
    def __init__(self):
        super(SpatialAttentionModule3, self).__init__()
        self.conv2d = nn.Conv2d(in_channels=2, out_channels=1, kernel_size=7, stride=1, padding=3)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # map尺寸不变，缩减通道
        avgout = torch.mean(x, dim=1, keepdim=True)
        maxout, _ = torch.max(x, dim=1, keepdim=True)
        print(avgout.size())
        out = torch.cat([avgout, maxout], dim=1)
        out = self.sigmoid(self.conv2d(out))
        print(out.size())
        return out


def test():
    net = SpatialAttentionModule2()
    x = torch.randn(2, 3, 32, 32)
    y = net(x)
    print(y.size())


test()
