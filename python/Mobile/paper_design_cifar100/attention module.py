import torch
from torch import nn


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
        avgout = self.shared_MLP(self.avg_pool(x))
        maxout = self.shared_MLP(self.max_pool(x))
        return self.sigmoid(avgout + maxout)


class SpatialAttentionModule(nn.Module):
    def __init__(self):
        super(SpatialAttentionModule, self).__init__()
        # self.conv2d = nn.Conv2d(in_channels=2, out_channels=1, kernel_size=7, stride=1, padding=3)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # map尺寸不变，缩减通道
        # avgout = torch.mean(x, dim=1, keepdim=True)
        maxout, _ = torch.max(x, dim=1, keepdim=True)
        # out = torch.cat([avgout, maxout], dim=1)
        # out = self.sigmoid(self.conv2d(out))
        out = self.sigmoid(maxout)
        return out


class Squeeze(nn.Module):  # 第二种
    def __init__(self, channel, reduction=16):
        super(Squeeze, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // reduction, channel, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)


#  第一种
class SeModule(nn.Module):
    def __init__(self, channel):
        super(SeModule, self).__init__()
        self.channel_attention = ChannelAttentionModule(channel)
        self.spatial_attention = SpatialAttentionModule()

    def forward(self, x):
        out1 = self.channel_attention(x) * x
        out2 = self.spatial_attention(x) * x
        out1 = out1 + out2
        return out1


#  第一种
class SeModule(nn.Module):
    def __init__(self, channel):
        super(SeModule, self).__init__()
        self.channel_attention = Squeeze(channel)
        self.spatial_attention = SpatialAttentionModule()

    def forward(self, x):
        out1 = self.channel_attention(x) * x
        out2 = self.spatial_attention(x) * x
        out1 = out1 + out2
        return out1



'''V1_mix_try_1 67.09'''
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
    def __init__(self, ):
        super(SpatialAttentionModule, self).__init__()
        self.conv2d = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=5, stride=1, padding=2)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # map尺寸不变，缩减通道
        avgout = torch.mean(x, dim=1, keepdim=True)
        maxout, _ = torch.max(x, dim=1, keepdim=True)
        # out = torch.cat([avgout, maxout], dim=1)
        # out = self.sigmoid(self.conv2d(out))
        out = maxout + avgout
        out = self.sigmoid(self.conv2d(out))
        return out


class SeModule(nn.Module):
    def __init__(self, channel):
        super(SeModule, self).__init__()
        self.channel_attention = ChannelAttentionModule(channel)
        self.spatial_attention = SpatialAttentionModule()

    def forward(self, x):
        out1 = self.channel_attention(x) * x
        out2 = self.spatial_attention(x) * x
        return (out1 + out2 + x)


# up 67.56 middle 67.95
class ChannelAttentionModule(nn.Module):  # 第二种
    def __init__(self, channel, reduction=4):
        super(ChannelAttentionModule, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // reduction, channel, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)


class SpatialAttentionModule(nn.Module):
    def __init__(self, ):
        super(SpatialAttentionModule, self).__init__()
        self.conv2d = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=5, stride=1, padding=2)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # map尺寸不变，缩减通道
        avgout = torch.mean(x, dim=1, keepdim=True)
        maxout, _ = torch.max(x, dim=1, keepdim=True)
        # out = torch.cat([avgout, maxout], dim=1)
        # out = self.sigmoid(self.conv2d(out))
        out = maxout + avgout
        out = self.sigmoid(self.conv2d(out))
        return out


class SeModule(nn.Module):
    def __init__(self, channel):
        super(SeModule, self).__init__()
        self.channel_attention = ChannelAttentionModule(channel)
        self.spatial_attention = SpatialAttentionModule()

    def forward(self, x):
        out1 = self.channel_attention(x)
        out2 = self.spatial_attention(x) * x
        return (out1 + out2)


# V1 se 2 cbam 31 68.09
class ChannelAttentionModule(nn.Module):  # 第二种
    def __init__(self, channel, reduction=4):
        super(ChannelAttentionModule, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // reduction, channel, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)


class SpatialAttentionModule(nn.Module):
    def __init__(self):
        super(SpatialAttentionModule, self).__init__()
        self.conv2d = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, stride=1, padding=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # map尺寸不变，缩减通道
        avgout = torch.mean(x, dim=1, keepdim=True)
        maxout, _ = torch.max(x, dim=1, keepdim=True)
        # out = torch.cat([avgout, maxout], dim=1)
        # out = self.sigmoid(self.conv2d(out))
        out = maxout + avgout
        out = self.sigmoid(self.conv2d(out))
        return out


class SeModule(nn.Module):
    def __init__(self, channel):
        super(SeModule, self).__init__()
        self.channel_attention = ChannelAttentionModule(channel)
        self.spatial_attention = SpatialAttentionModule()

    def forward(self, x):
        out1 = self.channel_attention(x)
        out2 = self.spatial_attention(x) * x
        return out1 + out2