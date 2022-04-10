from torch import Tensor
import torch.nn.functional as F
from torch.autograd import Variable
import torch
import math
#
# #
# #
# # # cx = Variable(torch.zeros(1, 512))
# # # hx = Tensor(torch.zeros(1, 512))
# # #
# # # print(cx)
# # # print(hx)
# # #
# # # h_out = (torch.zeros([1, 1, 512], dtype=torch.float32),
# # #                      torch.zeros([1, 1, 512],  dtype=torch.float32))
# # #
# # # print(h_out)
# # # torch.manual_seed(1)
# #
# # q = Variable(torch.rand(2, 10))
# # k = Variable(torch.rand(1, 10))
# # v = q
# # # v = Variable(torch.rand(1, 10))
# #
# # def attention(query, key, value, mask=None, dropout=None):
# #     "Compute 'Scaled Dot Product Attention'"
# #     d_k = query.size(-1)
# #     scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
# #     if mask is not None:
# #         scores = scores.masked_fill(mask == 0, -1e9)
# #     p_attn = F.softmax(scores, dim=-1)
# #     if dropout is not None:
# #         p_attn = dropout(p_attn)
# #     return torch.matmul(p_attn, value), p_attn
# #
# # r , p = attention(q,k,v)
# #
# # print(r)
#
# # a = [1, 2, 3]
#
# # b = a[0:-1]
#
# # print(b)
#
# # hx = Tensor(torch.zeros(1, 2))
# # ax = Tensor(torch.ones(1, 2))
# # bx = Tensor(torch.zeros(1, 2))
# #
# # cx = torch.cat((hx,ax),0)
# #
# # dx = torch.cat((cx,bx),0)
# #
# # print(cx,dx)
#
#
# # a = torch.Tensor([[1, 2],
# #                   [3, 4]])
# #
# # b = torch.gather(a, 1, torch.LongTensor([[0, 0], [1, 0]]))
# # # 1. 取各个元素行号：[(0,y)(0,y)][(1,y)(1,y)]
# # # 2. 取各个元素值做行号：[(0,0)(0,0)][(1,1)(1,0)]
# # # 3. 根据得到的索引在输入中取值
# # # [1,1],[4,3]
# #
# # c = torch.gather(a, 0, torch.LongTensor([[0, 0], [1, 0]]))
# # # 1. 取各个元素列号：[(x,0)(x,1)][(x,0)(x,1)]
# # # 2. 取各个元素值做行号：[(0,0)(0,1)][(1,0)(0,1)]
# # # 3. 根据得到的索引在输入中取值
# # # [1,2],[3,2]
#
# a = torch.Tensor([[0, 1, 2],
#                   [3, 4, 5],
#                   [6, 7, 8],
#                   [9, 10, 11],
#                   [12, 13, 14]])
#
# index = torch.LongTensor([[2, 1, 0, 1 ,2]])  # 这里index和input必须有一样的维度...
# index = index.view(-1,1)
# b = torch.gather(a, 1, index)
# # tensor([[6, 4, 2]])
# print(b)

# index = torch.Tensor([-0.5])  # 这里index和input必须有一样的维度...
# print(torch.exp(index))
# import numpy as np
#
# a = np.array([[1, 2], [3, 4]])
# b = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
# # a = b
# b=b.reshape(3,3)
# # print(a)
# print(b)

print("save new model Agent_%s"%1)
