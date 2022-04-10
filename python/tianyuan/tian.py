import megengine as mge
import megengine.functional as F
import numpy as np

def two_layer_conv(x):
    # (8, 3, 3, 3) 代表（输出信道数，输入信道数，卷积核高度，卷积核宽度）
    conv_weight = mge.Parameter(np.random.randn(8, 3, 3, 3).astype(np.float32))
    # 对于 8 个卷积核，提供 8 个 bias
    conv_bias = mge.Parameter(np.zeros((1, 8, 1, 1), dtype=np.float32))
    x = F.conv2d(x, conv_weight, conv_bias)
    x = F.relu(x)
    conv_weight = mge.Parameter(np.random.randn(16, 8, 3, 3).astype(np.float32))
    conv_bias = mge.Parameter(np.zeros((1, 16, 1, 1), dtype=np.float32))
    x = F.conv2d(x, conv_weight, conv_bias)
    x = F.relu(x)
    return x

# 输入形状为 (2, 3, 32, 32) 的张量
x = mge.tensor(np.random.randn(2, 3, 32, 32).astype(np.float32))
out = two_layer_conv(x)
print(out.shape)  # 输出： (2, 16, 28, 28)
