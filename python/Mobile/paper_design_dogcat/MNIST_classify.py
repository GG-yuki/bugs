'''
/********************************************************************
*
*  文件名：test.py
*
*  文件描述：卷积神经网络 kaggle mnist 手写数字识别
*
*  创建人： qiwei_ji, 2020年3月17日
*
*  版本号：1.1.3.0317_alpha
*
*  修改记录：62
*
********************************************************************/
'''


# import numpy as np
# import pandas as pd
# import torch
# import torch.nn as nn
# from torch.autograd import Variable
# import torch.utils.data as Data
# import matplotlib.pyplot as plt
# import torch.nn.functional as F
# import csv
from support import *
from mobilenetv1 import mobiletnetv1
from mobilenetv2 import mobiletNetv2
import datetime
import time


# Hyper Parameters
EOPCH = 30             # 几个世纪
BATCH_SIZE = 64
LR = 0.001              # learning rate


#计算时间，开始运行
starttime = datetime.datetime.now()

#实例化
cnn = mobilenetv1()
#print(cnn)  # net architecture
optimzer = torch.optim.Adam(cnn.parameters(),lr=LR) # define optimezer
loss_func = nn.CrossEntropyLoss()   # define loss_function 交叉嫡误差


# 加载训练数据集
train= pd.read_csv('train.csv')
train_labels__ = torch.from_numpy(np.array(train.label[:]))#42000,数字，read读取时自动把第一行当列名
train_data__ = torch.FloatTensor(np.array(train.iloc[:,1:]).reshape((-1,1,28,28)))/255#42000*784，除以255
#print(train_data__.size())


# 加载测试数据集
print(train_data__.type())
test= pd.read_csv('test.csv')
test_data = torch.FloatTensor(np.array(test).reshape((-1,1,28,28)))/255#28000
#print(test_data.size())


#批处理
train_data = Data.TensorDataset(train_data__,train_labels__)
train_loader = Data.DataLoader(
    dataset=train_data,
    batch_size=BATCH_SIZE,
    shuffle=True
)


#装载结束
print('load data is over')


#展示第一幅图像
# plt.imshow(train_data__[1].squeeze().numpy(),cmap='gray')
# plt.title('%i' % train_labels__[1])
# plt.show()


#训练数据
for epoch in range(EOPCH):
    for step,(x,y) in enumerate(train_loader):  # gives batch data
        b_x = Variable(x)
        b_y = Variable(y)
        output = cnn(b_x)   # cnn output
        loss = loss_func(output,b_y)    # cross entropy loss
        # update W
        optimzer.zero_grad()
        loss.backward()
        optimzer.step()
        print('epoch %d'%(epoch+1),'start %d'%step)
#    print('train is over')


#预测并生成excel
test = cnn(test_data[:])
pred_test = torch.max(test,1)[1].squeeze()
out = pd.DataFrame(np.array(pred_test),index=range(1,1+len(pred_test)),columns=['Label'])
out.columns.name = 'ImageId'
out.to_csv('nope.csv',header=True,index=True,index_label='ImageId')
# print('done')


#计算时间，结束运行
endtime = datetime.datetime.now()
print ((endtime - starttime).seconds)