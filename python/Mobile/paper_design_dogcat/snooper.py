#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import numpy as np
import torch

import pysnooper

def large(l):
    return isinstance(l, list) and len(l) > 5

def print_list_size(l):
    return 'list(size={})'.format(len(l))

def print_ndarray(a):
    return 'ndarray(shape={}, dtype={})'.format(a.shape, a.dtype)

def print_tensor(tensor):
    return 'torch.Tensor(shape={}, dtype={}, device={})'.format(tensor.shape, tensor.dtype, tensor.device)

custom_repr = ((large, print_list_size), (np.ndarray, print_ndarray), (torch.Tensor, print_tensor))


snooper_config = {

    'custom_repr' : custom_repr,

}

my_snooper = pysnooper.snoop('debug.log', **snooper_config)