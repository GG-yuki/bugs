import mindspore.nn as nn
from mindspore.common.initializer import TruncatedNormal
from mindspore import context
import argparse


def env():
    #配置运行环境
    parser = argparse.ArgumentParser(description='MindSpore LeNet Example')
    parser.add_argument('--device_target', type=str, default="CPU", choices=['CPU'],#3个选项，分别为'Ascend', 'GPU', 'CPU'
                            help='device where the code will be implemented (default: CPU)')
    args = parser.parse_args()
    context.set_context(mode=context.GRAPH_MODE, device_target=args.device_target)
    dataset_sink_mode = not args.device_target == "CPU"

def weight_variable():
    """
    weight initial
    """
    return TruncatedNormal(0.02)

def conv(in_channels, out_channels, kernel_size, stride=0, padding=0):
    """
    conv layer weight initial
    """
    weight = weight_variable()
    return nn.Conv2d(in_channels, out_channels,
                     kernel_size=kernel_size, stride=stride, padding=padding,
                     weight_init=weight, has_bias=False, pad_mode="valid")

def fc(input_channels, out_channels):
    """
    fc layer weight initial
    """
    weight = weight_variable()
    bias = weight_variable()
    return nn.Dense(input_channels, out_channels, weight, bias)

def bn(channel):
    return nn.BatchNorm2d(channel, eps=1e-4, momentum=0.9,
                        gamma_init=1, beta_init=0, moving_mean_init=0, moving_var_init=1)