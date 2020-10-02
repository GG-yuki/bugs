from mindspore import Tensor
import numpy as np
from support import *
from mindspore import float32

env()#设置运行环境，目前是使用cpu，可进入support文件畸形修改

class Segnet(nn.Cell):
    """
    Lenet network structure
    """
    #define the operator required


    # Encoder
    def __init__(self, input_nc, output_nc):
        super(Segnet, self).__init__()

        self.conv11 = conv(input_nc, 64, kernel_size=3, padding=1)
        self.bn11 = bn(64)
        self.conv12 = conv(64, 64, 3, 0, padding=1)
        self.bn12 = bn(64)

        self.conv21 = nn.conv(64, 128, kernel_size=3, padding=1)
        self.bn21 = nn.bn(128)
        self.conv22 = nn.conv(128, 128, kernel_size=3, padding=1)
        self.bn22 = nn.bn(128)

        self.conv31 = nn.conv(128, 256, kernel_size=3, padding=1)
        self.bn31 = nn.bn(256)
        self.conv32 = nn.conv(256, 256, kernel_size=3, padding=1)
        self.bn32 = nn.bn(256)
        self.conv33 = nn.conv(256, 256, kernel_size=3, padding=1)
        self.bn33 = nn.bn(256)

        self.conv41 = nn.conv(256, 512, kernel_size=3, padding=1)
        self.bn41 = nn.bn(512)
        self.conv42 = nn.conv(512, 512, kernel_size=3, padding=1)
        self.bn42 = nn.bn(512)
        self.conv43 = nn.conv(512, 512, kernel_size=3, padding=1)
        self.bn43 = nn.bn(512)

        self.conv51 = nn.conv(512, 512, kernel_size=3, padding=1)
        self.bn51 = nn.bn(512)
        self.conv52 = nn.conv(512, 512, kernel_size=3, padding=1)
        self.bn52 = nn.bn(512)
        self.conv53 = nn.conv(512, 512, kernel_size=3, padding=1)
        self.bn53 = nn.bn(512)

        # Decoder
        self.conv53d = nn.conv(512, 512, kernel_size=3, padding=1)
        self.bn53d = nn.bn(512)
        self.conv52d = nn.conv(512, 512, kernel_size=3, padding=1)
        self.bn52d = nn.bn(512)
        self.conv51d = nn.conv(512, 512, kernel_size=3, padding=1)
        self.bn51d = nn.bn(512)

        self.conv43d = nn.conv(512, 512, kernel_size=3, padding=1)
        self.bn43d = nn.bn(512)
        self.conv42d = nn.conv(512, 512, kernel_size=3, padding=1)
        self.bn42d = nn.bn(512)
        self.conv41d = nn.conv(512, 256, kernel_size=3, padding=1)
        self.bn41d = nn.bn(256)

        self.conv33d = nn.conv(256, 256, kernel_size=3, padding=1)
        self.bn33d = nn.bn(256)
        self.conv32d = nn.conv(256, 256, kernel_size=3, padding=1)
        self.bn32d = nn.bn(256)
        self.conv31d = nn.conv(256, 128, kernel_size=3, padding=1)
        self.bn31d = nn.bn(128)

        self.conv22d = nn.conv(128, 128, kernel_size=3, padding=1)
        self.bn22d = nn.bn(128)
        self.conv21d = nn.conv(128, 64, kernel_size=3, padding=1)
        self.bn21d = nn.bn(64)

        self.conv12d = nn.conv(64, 64, kernel_size=3, padding=1)
        self.bn12d = nn.bn(64)
        self.conv11d = nn.conv(64, output_nc, kernel_size=3, padding=1)


    def forward(self, x):
        # Stage 1
        x11 = nn.relu(self.bn11(self.conv11(x)))
        x12 = nn.relu(self.bn12(self.conv12(x11)))
        x1p, id1 = nn.MaxPool2d(x12, kernel_size=2, stride=2, return_indices=True)

        # Stage 2
        x21 = nn.relu(self.bn21(self.conv21(x1p)))
        x22 = nn.relu(self.bn22(self.conv22(x21)))
        x2p, id2 = nn.MaxPool2d(x22, kernel_size=2, stride=2, return_indices=True)

        # Stage 3
        x31 = nn.relu(self.bn31(self.conv31(x2p)))
        x32 = nn.relu(self.bn32(self.conv32(x31)))
        x33 = nn.relu(self.bn33(self.conv33(x32)))
        x3p, id3 = nn.MaxPool2d(x33, kernel_size=2, stride=2, return_indices=True)

        # Stage 4
        x41 = nn.relu(self.bn41(self.conv41(x3p)))
        x42 = nn.relu(self.bn42(self.conv42(x41)))
        x43 = nn.relu(self.bn43(self.conv43(x42)))
        x4p, id4 = nn.MaxPool2d(x43, kernel_size=2, stride=2, return_indices=True)

        # Stage 5
        x51 = nn.relu(self.bn51(self.conv51(x4p)))
        x52 = nn.relu(self.bn52(self.conv52(x51)))
        x53 = nn.relu(self.bn53(self.conv53(x52)))
        x5p, id5 = nn.MaxPool2d(x53, kernel_size=2, stride=2, return_indices=True)

        # Stage 5d
        x5d = F.max_unpool2d(x5p, id5, kernel_size=2, stride=2)
        x53d = nn.relu(self.bn53d(self.conv53d(x5d)))
        x52d = nn.relu(self.bn52d(self.conv52d(x53d)))
        x51d = nn.relu(self.bn51d(self.conv51d(x52d)))

        # Stage 4d
        x4d = F.max_unpool2d(x51d, id4, kernel_size=2, stride=2)
        x43d = nn.relu(self.bn43d(self.conv43d(x4d)))
        x42d = nn.relu(self.bn42d(self.conv42d(x43d)))
        x41d = nn.relu(self.bn41d(self.conv41d(x42d)))

        # Stage 3d
        x3d = F.max_unpool2d(x41d, id3, kernel_size=2, stride=2)
        x33d = nn.relu(self.bn33d(self.conv33d(x3d)))
        x32d = nn.relu(self.bn32d(self.conv32d(x33d)))
        x31d = nn.relu(self.bn31d(self.conv31d(x32d)))

        # Stage 2d
        x2d = F.max_unpool2d(x31d, id2, kernel_size=2, stride=2)
        x22d = nn.relu(self.bn22d(self.conv22d(x2d)))
        x21d = nn.relu(self.bn21d(self.conv21d(x22d)))

        # Stage 1d
        x1d = F.max_unpool2d(x21d, id1, kernel_size=2, stride=2)
        x12d = nn.relu(self.bn12d(self.conv12d(x1d)))  ##需要激活函数吗？
        x11d = self.conv11d(x12d)  ##是不是少了bn层？
        output = t.sigmoid(x11d)  ##sigmoid和softmax和全连接的区别？  #本来这应该是是一个像素分类层？

        return output



a = Tensor(np.ones([2, 1, 32, 32]), float32)
lenet = LeNet5()
out = lenet(a)
print (out)




MaxPoolWithArgmax