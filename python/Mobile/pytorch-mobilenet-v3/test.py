import torch
import torch.nn as nn
import torch.nn.functional as F


class Identity(nn.Module):
    def __init__(self, channel):
        super(Identity, self).__init__()

    def forward(self, x):
        return x


class MobileBottleneck(nn.Module):
    def __init__(self, exp, se=False):
        super(MobileBottleneck, self).__init__()
        if se:
            SELayer = SEModule
        else:
            SELayer = Identity

        self.conv = nn.Sequential(
            SELayer(exp),
        )

    def forward(self, x):
        return self.conv(x)

net = MobileBottleneck(2,False)
x = torch.randn(1,1,2,3)
print(x)
y = net(x)
print(y)