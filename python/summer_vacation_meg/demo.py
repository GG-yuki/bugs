import megengine as mge
import megengine.functional as F
import numpy as np
import megengine.module as M


class mobilenetv1(M.Module):
    def __init__(self):
        super(mobilenetv1, self).__init__()
        def conv_bn(inp, oup, stride):
            return M.Sequential(
                M.Conv2d(inp, oup, 3, stride, 1),
                M.BatchNorm2d(oup),
                M.ReLU()
            )

        def conv_dw(inp, oup, stride):
            return M.Sequential(
                M.Conv2d(inp, inp, 3, stride, 1, groups=inp),
                M.BatchNorm2d(inp),
                M.ReLU(),

                M.Conv2d(inp, oup, 1, 1, 0),
                M.BatchNorm2d(oup),
                M.ReLU(),
            )
        self.model = M.Sequential(
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
            M.AvgPool2d(7),
        )
        self.fc1 = M.Linear(1024, 1000)
        self.fc2 = M.Linear(1000, 10)

    def forward(self, x):
        x = self.model(x)
        x = F.flatten(x, 1)
        x = self.fc1(x)
        x = self.fc2(x)
        return x




# 输入形状为 (2, 1, 32, 32) 的张量
x = mge.tensor(np.random.randn(2, 3, 224, 224).astype(np.float32))
Mobile = mobilenetv1()
# 调用网络，即执行 le_net 的 forward 成员方法，返回网络处理结果
out = Mobile(x)
print(out.shape)  # 输出： (2, 10)