import torch.nn as nn
from torch.nn import init
import torch
import torch.nn.functional as F


class Classifier(torch.nn.Module):
    def __init__(self, in_channels, num_classes):
        super().__init__()
        self.conv = torch.nn.Conv2d(
            in_channels=in_channels,
            out_channels=num_classes,
            kernel_size=1,
            bias=True)

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        return x

    def init_params(self):
        torch.nn.init.xavier_normal_(self.conv.weight, gain=1.0)


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
        out1 = self.spatial_attention(out1) * out1
        return out1


# class ChannelAttentionModule(nn.Module):
#     def __init__(self, channel, ratio=16):
#         super(ChannelAttentionModule, self).__init__()
#         self.avg_pool = nn.AdaptiveAvgPool2d(1)
#         self.max_pool = nn.AdaptiveMaxPool2d(1)
#
#         self.shared_MLP = nn.Sequential(
#             nn.Conv2d(channel, channel // ratio, 1, bias=False),
#             nn.ReLU(),
#             nn.Conv2d(channel // ratio, channel, 1, bias=False)
#         )
#         self.sigmoid = nn.Sigmoid()
#
#     def forward(self, x):
#         avgout = self.shared_MLP(self.avg_pool(x))
#         print(avgout.shape)
#         maxout = self.shared_MLP(self.max_pool(x))
#         return self.sigmoid(avgout + maxout)
#
#
# class SpatialAttentionModule(nn.Module):
#     def __init__(self):
#         super(SpatialAttentionModule, self).__init__()
#         self.conv2d = nn.Conv2d(in_channels=2, out_channels=1, kernel_size=7, stride=1, padding=3)
#         self.sigmoid = nn.Sigmoid()
#
#     def forward(self, x):
#         avgout = torch.mean(x, dim=1, keepdim=True)
#         maxout, _ = torch.max(x, dim=1, keepdim=True)
#         out = torch.cat([avgout, maxout], dim=1)
#         out = self.sigmoid(self.conv2d(out))
#         return out
#
#
# class SeModule(nn.Module):
#     def __init__(self, channel):
#         super(SeModule, self).__init__()
#         self.channel_attention = ChannelAttentionModule(channel)
#         self.spatial_attention = SpatialAttentionModule()
#
#     def forward(self, x):
#         out = self.channel_attention(x) * x
#         print('outchannels:{}'.format(out.shape))
#         out = self.spatial_attention(out) * out
#         return out


# class hsigmoid(nn.Module):
#     def forward(self, x):
#         out = F.relu6(x + 3, inplace=True) / 6
#         return out
#
#
# class SeModule(nn.Module):
#     def __init__(self, in_size, reduction=4):
#         super(SeModule, self).__init__()
#
#         self.se = nn.Sequential(
#             nn.AdaptiveAvgPool2d(1),
#             nn.Conv2d(in_size, in_size // reduction, kernel_size=1, stride=1, padding=0, bias=False),
#             nn.BatchNorm2d(in_size // reduction),
#             nn.ReLU(inplace=True),
#             nn.Conv2d(in_size // reduction, in_size, kernel_size=1, stride=1, padding=0, bias=False),
#             nn.BatchNorm2d(in_size),
#             hsigmoid()
#         )
#
#     def forward(self, x):
#         return x * self.se(x)


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
                # SeModule(inp),
                nn.Conv2d(inp, inp, 3, stride, 1, groups=inp, bias=False),
                nn.BatchNorm2d(inp),
                nn.ReLU(inplace=True),
                SeModule(inp),
                nn.Conv2d(inp, oup, 1, 1, 0, bias=False),
                nn.BatchNorm2d(oup),
                nn.ReLU(inplace=True),
                # SeModule(oup),
            )

        self.model = nn.Sequential(
            conv_bn(3, 32, 1),
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
        self.classifier = Classifier(in_channels=1024, num_classes=num_classes)
        self.init_params()

    def forward(self, x):
        x = self.model(x)
        x = self.avg(x)
        x = self.classifier(x)
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

        self.classifier.init_params()


def test():
    net = MobileNetV1(10)
    x = torch.randn(2, 3, 32, 32)
    y = net(x)
    torch.save(net.state_dict(), './pkl/net_params.pkl')
    print(y.size())
    from thop import profile
    flops, params = profile(net, inputs=(x, ))
    print('flops:', flops)



test()


# class ChannelAttentionModule(nn.Module):  # 第二种
#     def __init__(self, channel, reduction=4):
#         super(ChannelAttentionModule, self).__init__()
#         self.avg_pool = nn.AdaptiveAvgPool2d(1)
#         self.mean_pool = nn.AdaptiveMaxPool2d(1)
#         self.fc = nn.Sequential(
#             nn.Linear(channel, channel // reduction, bias=False),
#             nn.ReLU(inplace=True),
#             nn.Linear(channel // reduction, channel, bias=False),
#             nn.Sigmoid()
#         )
#
#     def forward(self, x):
#         b, c, _, _ = x.size()
#         y = self.avg_pool(x) + self.mean_pool(x)
#         y = y.view(b, c)
#         y = self.fc(y).view(b, c, 1, 1)
#         return x * y.expand_as(x)