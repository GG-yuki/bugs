# from mindspore import Tensor
# import numpy as np
# from support import *
# from mindspore import float32
# import torch
# from support import *
# from torch import nn
# from torch import functional as F
#
# x = torch.tensor([[[[1,2,3],[4,5,6],[7,8,9]]]],dtype=torch.float32)
# a = nn.Conv2d(1,6,2)
# x = a(x)
# b = nn.MaxPool2d(kernel_size=2, stride=1, return_indices=True)
# x1,x2 = b(x)
# c = nn.MaxUnpool2d(kernel_size=2, stride=2)
# x = c(x1,x2)
# print(x)

import torch
import numpy as np

poolin = torch.nn.MaxPool2d(2,stride=1,return_indices=True)
unpoolin = torch.nn.MaxUnpool2d(2,stride=2)

def unpool_with_argmax(pool, ind, shape_ori, name = None, ksize=[1, 2, 2, 1]):

    """
       Unpooling layer after max_pool_with_argmax.
       Args:
           pool:   max pooled output tensor
           ind:      argmax indices
           ksize:     ksize is the same as for the pool
       Return:
           unpool:    unpooling tensor
    """
    with torch.variable_scope(name):
        input_shape = list(pool.size())
        output_shape = shape_ori
        flat_input_size = np.prod(input_shape)
        flat_output_shape = [output_shape[0], output_shape[1] * output_shape[2] * output_shape[3]]

        pool_ = torch.reshape(pool, [flat_input_size])
        batch_range = torch.reshape(torch.range(output_shape[0], dtype=ind.dtype), shape=[input_shape[0], 1, 1, 1])
        b = torch.ones_like(ind) * batch_range
        #first let's create batch matrix, the batch_range determine the batch index for each element in the matrix(0,to,batch_size-1),
        #the size will be as same as the size of output from maxpooling! And also when we reshape the output(if the batch size is not 1), then the order of
        #output  is first read from the first batch, after finished we start to read the second batch, so this way is exactly does the same thing, the
        #concat index for the first batch are all zero, then the concat index for the second batch are all one, so this upsampling way is really correct!!
        #actually the flattened pooling index represent the index for the pooling value, which is in the range of (0-totalnumber of pixels)!!
        b = torch.reshape(b, [flat_input_size, 1])
        ind_ = torch.reshape(ind, [flat_input_size, 1])
        ind_ = torch.cat([b, ind_], 1)
        ret = torch.scatter(ind_, pool_, shape=flat_output_shape)
        ret = torch.reshape(ret, output_shape)
        return ret


gen_array = torch.tensor([[[[0, 1, 3,4],
                        [1, 3, 6,5],
                        [2, 6, 7,6],
                        [3, 7, 2,7]],

                       [[7, 4, 1,2],
                        [8, 9, 9,8],
                        [5, 8, 2,0],
                        [3, 5, 8,7]],

                       [[2, 6, 2,7],
                        [4, 3, 7,9],
                        [3, 2, 3,3],
                        [9, 5, 5,4]],

                       [[7, 3, 1,2],
                        [4, 7, 4,9],
                        [6, 5, 6,3],
                        [7, 8, 9,7]]]],dtype=float)

ouputin , indicesin = poolin(gen_array)

x = unpoolin(ouputin,indicesin)
print(x)
x = un