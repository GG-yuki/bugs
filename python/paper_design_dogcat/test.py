#  # coding=utf-8
# import os
# import numpy as np
# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import torch.optim as optim
# from torch.autograd import Variable
# from torch.utils.data import Dataset
# from torchvision import transforms, datasets, models
#
#
# # kaggle原始数据集地址
# original_dataset_dir = r'C:\Users\Yuki\Desktop\bugs\python\graduation_design\New folder\train'
# total_num = int(len(os.listdir(original_dataset_dir)) / 2)
# random_idx = np.array(range(total_num))
# np.random.shuffle(random_idx)
#
#
# epochs = 10 # 训练次数
# batch_size = 4  # 批处理大小
# num_workers = 0  # 多线程的数目
#
#
# # 对加载的图像作归一化处理， 并裁剪为[224x224x3]大小的图像89ta_
# transform = transforms.Compose([
#     transforms.Resize(256),
#     transforms.CenterCrop(224),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
# ])
#
# train_dataset = datasets.ImageFolder(root=r'C:\Users\Yuki\Desktop\bugs\python\graduation_design\New folder\train',
#                                      transform=data_transform)
# train_loader = torch.utils.data.DataLoader(train_dataset,
#                                            batch_size=batch_size,
#                                            shuffle=True,
#                                            num_workers=num_workers)
#
# test_dataset = datasets.ImageFolder(root=r'C:\Users\Yuki\Desktop\bugs\python\graduation_design\New folder\test', transform=data_transform)
# test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
#
#
# # 创建模型
# class Net(nn.Module):
#     def __init__(self):
#         super(Net, self).__init__()
#         self.conv1 = nn.Conv2d(3, 6, 5)
#         self.maxpool = nn.MaxPool2d(2, 2)
#         self.conv2 = nn.Conv2d(6, 16, 5)
#         self.fc1 = nn.Linear(16 * 53 * 53, 1024)
#         self.fc2 = nn.Linear(1024, 512)
#         self.fc3 = nn.Linear(512, 2)
#
#     def forward(self, x):
#         x = self.maxpool(F.relu(self.conv1(x)))
#         x = self.maxpool(F.relu(self.conv2(x)))
#         x = x.view(-1, 16 * 53 * 53)
#         x = F.relu(self.fc1(x))
#         x = F.relu(self.fc2(x))
#         x = self.fc3(x)
#         return x
#
#
# net = Net()
#
# print(net)
#
# # 定义loss和optimizer
# cirterion = nn.CrossEntropyLoss()
# optimizer = optim.SGD(net.parameters(), lr=0.0001, momentum=0.9)
#
# def train():
#
#     for epoch in range(epochs):
#         running_loss = 0.0
#         train_correct = 0
#         train_total = 0
#         print("yes\n")
#         for i, data in enumerate(train_loader, 0):
#             inputs, train_labels = data
#             inputs, labels = Variable(inputs), Variable(train_labels)
#             optimizer.zero_grad()
#             outputs = net(inputs)
#             _, train_predicted = torch.max(outputs.data, 1)
#             train_correct += (train_predicted == labels.data).sum()
#             loss = cirterion(outputs, labels)
#             loss.backward()
#             optimizer.step()
#             running_loss += loss.item()
#             train_total += train_labels.size(0)
#             # print("%d\n",i)
#         print('train %d epoch loss: %.3f  acc: %.3f ' % (
#             epoch + 1, running_loss / train_total, 100 * train_correct / train_total))
#         # 模型测试
#         correct = 0
#         test_loss = 0.0
#         test_total = 0
#         net.eval()
#         for data in test_loader:
#             images, labels = data
#             images, labels = Variable(images), Variable(labels)
#             outputs = net(images)
#             # predicted = torch.max(outputs.data, 1)
#             _, predicted = torch.max(outputs.data, 1)
#             loss = cirterion(outputs, labels)
#             test_loss += loss.item()
#             test_total += labels.size(0)
#             correct += (predicted == labels.data).sum()
#         print('test  %d epoch loss: %.3f  acc: %.3f ' % (epoch + 1, test_loss / test_total, 100 * correct / test_total))
#
# train()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # coding=utf-8
# import os
# import numpy as np
# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import torch.optim as optim
# from torch.autograd import Variable
# from torch.utils.data import Dataset
# from torchvision import transforms, datasets, models
#
# # 随机种子设置
# random_state = 42
# np.random.seed(random_state)
#
# # kaggle原始数据集地址
# original_dataset_dir = 'E:\python ese\c_d\data\\train\\train'
# total_num = int(len(os.listdir(original_dataset_dir)) / 2)
# random_idx = np.array(range(total_num))
# np.random.shuffle(random_idx)
#
# # 待处理的数据集地址
# base_dir = 'E:\python ese\c_d\data2'
# if not os.path.exists(base_dir):
#     os.mkdir(base_dir)
#
# # 训练集、测试集的划分
# sub_dirs = ['train', 'test']
# animals = ['cats', 'dogs']
# train_idx = random_idx[:int(total_num * 0.9)]
# test_idx = random_idx[int(total_num * 0.9):]
# numbers = [train_idx, test_idx]
# for idx, sub_dir in enumerate(sub_dirs):
#     dir = os.path.join(base_dir, sub_dir)
#     if not os.path.exists(dir):
#         os.mkdir(dir)
#     for animal in animals:
#         animal_dir = os.path.join(dir, animal)  #
#         if not os.path.exists(animal_dir):
#             os.mkdir(animal_dir)
#         fnames = [animal[:-1] + '.{}.jpg'.format(i) for i in numbers[idx]]
#         for fname in fnames:
#             src = os.path.join(original_dataset_dir, fname)
#             dst = os.path.join(animal_dir, fname)
#             shutil.copyfile(src, dst)
#
#         # 验证训练集、验证集、测试集的划分的照片数目
#         print(animal_dir + ' total images : %d' % (len(os.listdir(animal_dir))))
#     # coding=utf-8
#
# # 配置参数
# random_state = 1
# torch.manual_seed(random_state)  # 设置随机数种子，确保结果可重复
# torch.cuda.manual_seed(random_state)
# torch.cuda.manual_seed_all(random_state)
# np.random.seed(random_state)
# # random.seed(random_state)
#
# epochs = 10 # 训练次数
# batch_size = 4  # 批处理大小
# num_workers = 0  # 多线程的数目
# use_gpu = torch.cuda.is_available()
# PATH='E:\python ese\c_d\model.pt'
# # 对加载的图像作归一化处理， 并裁剪为[224x224x3]大小的图像
# data_transform = transforms.Compose([
#     transforms.Resize(256),
#     transforms.CenterCrop(224),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
# ])
#
# train_dataset = datasets.ImageFolder(root='./data2/train/',
#                                      transform=data_transform)
# train_loader = torch.utils.data.DataLoader(train_dataset,
#                                            batch_size=batch_size,
#                                            shuffle=True,
#                                            num_workers=num_workers)
#
# test_dataset = datasets.ImageFolder(root='./data2/test/', transform=data_transform)
# test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
#
#
# # 创建模型
# class Net(nn.Module):
#     def __init__(self):
#         super(Net, self).__init__()
#         self.conv1 = nn.Conv2d(3, 6, 5)
#         self.maxpool = nn.MaxPool2d(2, 2)
#         self.conv2 = nn.Conv2d(6, 16, 5)
#         self.fc1 = nn.Linear(16 * 53 * 53, 1024)
#         self.fc2 = nn.Linear(1024, 512)
#         self.fc3 = nn.Linear(512, 2)
#
#     def forward(self, x):
#         x = self.maxpool(F.relu(self.conv1(x)))
#         x = self.maxpool(F.relu(self.conv2(x)))
#         x = x.view(-1, 16 * 53 * 53)
#         x = F.relu(self.fc1(x))
#         x = F.relu(self.fc2(x))
#         x = self.fc3(x)
#
#         return x
#
#
# net = Net()
# if(os.path.exists('model.pt')):
#     net=torch.load('model.pt')
#
# if use_gpu:
#     net = net.cuda()
# print(net)
#
# # 定义loss和optimizer
# cirterion = nn.CrossEntropyLoss()
# optimizer = optim.SGD(net.parameters(), lr=0.0001, momentum=0.9)
#
# def train():
#
#     for epoch in range(epochs):
#         running_loss = 0.0
#         train_correct = 0
#         train_total = 0
#         for i, data in enumerate(train_loader, 0):
#             inputs, train_labels = data
#             if use_gpu:
#                 inputs, labels = Variable(inputs.cuda()), Variable(train_labels.cuda())
#             else:
#                 inputs, labels = Variable(inputs), Variable(train_labels)
#             optimizer.zero_grad()
#             outputs = net(inputs)
#             _, train_predicted = torch.max(outputs.data, 1)
#             train_correct += (train_predicted == labels.data).sum()
#             loss = cirterion(outputs, labels)
#             loss.backward()
#             optimizer.step()
#             running_loss += loss.item()
#             train_total += train_labels.size(0)
#
#         print('train %d epoch loss: %.3f  acc: %.3f ' % (
#             epoch + 1, running_loss / train_total, 100 * train_correct / train_total))
#         # 模型测试
#         correct = 0
#         test_loss = 0.0
#         test_total = 0
#         test_total = 0
#         net.eval()
#         for data in test_loader:
#             images, labels = data
#             if use_gpu:
#                 images, labels = Variable(images.cuda()), Variable(labels.cuda())
#             else:
#                 images, labels = Variable(images), Variable(labels)
#             outputs = net(images)
#             _, predicted = torch.max(outputs.data, 1)
#             loss = cirterion(outputs, labels)
#             test_loss += loss.item()
#             test_total += labels.size(0)
#             correct += (predicted == labels.data).sum()
#
#         print('test  %d epoch loss: %.3f  acc: %.3f ' % (epoch + 1, test_loss / test_total, 100 * correct / test_total))
#
#     torch.save(net, 'model.pt')
#
#
# train()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# import numpy as np
# import pandas as pd
# import torch
# import torch.nn as nn
# from torch.autograd import Variable
# import torch.utils.data as Data
# import matplotlib.pyplot as plt
# import torch.nn.functional as F
# import csv
# import datetime
# import time
#
# starttime = datetime.datetime.now()
#
# torch_dataset =torch.rand(100,3,224,224)
# y = torch.rand(100)
# train_data = Data.TensorDataset(torch_dataset,y)
# teach_dataset =torch.rand(2000,3,224,224)
#
# validation_loader = torch.utils.data.DataLoader(teach_dataset, batch_size=1)
#
# train_loader = Data.DataLoader(
#     dataset=train_data,      # torch TensorDataset format
#     batch_size=20,      # mini batch size
#     shuffle=True,               # random shuffle for training
# )
#
#
# class Net(nn.Module):
#     def __init__(self):
#         super(Net, self).__init__()
#
#         def conv_bn(inp, oup, stride):
#             return nn.Sequential(
#                 nn.Conv2d(inp, oup, 3, stride, 1, bias=False),
#                 nn.BatchNorm2d(oup),
#                 nn.ReLU(inplace=True)
#             )
#
#         def conv_dw(inp, oup, stride):
#             return nn.Sequential(
#                 nn.Conv2d(inp, inp, 3, stride, 1, groups=inp, bias=False),
#                 nn.BatchNorm2d(inp),
#                 nn.ReLU(inplace=True),
#
#                 nn.Conv2d(inp, oup, 1, 1, 0, bias=False),
#                 nn.BatchNorm2d(oup),
#                 nn.ReLU(inplace=True),
#             )
#
#         self.model = nn.Sequential(
#             conv_bn(3, 32, 2),
#             conv_dw(32, 64, 1),
#             conv_dw(64, 128, 2),
#             conv_dw(128, 128, 1),
#             conv_dw(128, 256, 2),
#             conv_dw(256, 256, 1),
#             conv_dw(256, 512, 2),
#             conv_dw(512, 512, 1),
#             conv_dw(512, 512, 1),
#             conv_dw(512, 512, 1),
#             conv_dw(512, 512, 1),
#             conv_dw(512, 512, 1),
#             conv_dw(512, 1024, 2),
#             conv_dw(1024, 1024, 1),
#             nn.AvgPool2d(7),
#         )
#         self.fc = nn.Linear(1024, 1)
#
#     def forward(self, x):
#         x = self.model(x)
#         x = x.view(-1, 1024)
#         x = self.fc(x)
#         output = F.softmax(x,dim=1)    # import torch.nn.funtional as F
#         return output
#
# class CNN(nn.Module):
#     def __init__(self):
#         super(CNN, self).__init__()
#
#         def conv_bn(inp, oup, stride):
#             return nn.Sequential(
#                 nn.Conv2d(inp, oup, 3, stride, 1, bias=False),
#                 nn.BatchNorm2d(oup),
#                 nn.ReLU(inplace=True)
#             )
#
#         self.model = nn.Sequential(
#             conv_bn(3, 32, 2),
#             conv_bn(32, 64, 1),
#             conv_bn(64, 128, 2),
#             conv_bn(128, 128, 1),
#             conv_bn(128, 256, 2),
#             conv_bn(256, 256, 1),
#             conv_bn(256, 512, 2),
#             conv_bn(512, 512, 1),
#             conv_bn(512, 512, 1),
#             conv_bn(512, 512, 1),
#             conv_bn(512, 512, 1),
#             conv_bn(512, 512, 1),
#             conv_bn(512, 1024, 2),
#             conv_bn(1024, 1024, 1),
#             nn.AvgPool2d(7),
#         )
#         self.fc = nn.Linear(1024, 1)
#
#     def forward(self, x):
#         x = self.model(x)
#         x = x.view(-1, 1024)
#         x = self.fc(x)
#         output = F.softmax(x,dim=1)    # import torch.nn.funtional as F
#         return output
#
# endtime2 = datetime.datetime.now()
# print ((endtime2 - starttime).seconds)
#
# LR = 0.001              # learning rate
# cnn = Net()
# # print(cnn)  # net architecture
# optimzer = torch.optim.Adam(cnn.parameters(),lr=LR) # define optimezer
# loss_func = nn.CrossEntropyLoss()   # define loss_function 交叉嫡误差
#
# # cnnnet=CNN()
# # optimzer = torch.optim.Adam(cnnnet.parameters(),lr=LR) # define optimezer
# # loss_func = nn.CrossEntropyLoss()   # define loss_function 交叉嫡误差
#
# for epoch in range(10):
#     for step,(x,y) in enumerate(train_loader):  # gives batch data
#         b_x = Variable(x)
#         b_y = Variable(y)
#         output = cnn(b_x)   # cnn output
#         # print(output.shape)
#         loss = loss_func(output,b_y.long())    # cross entropy loss
#         # update W
#         optimzer.zero_grad()
#         loss.backward()
#         optimzer.step()
#         print('epoch %d'%(epoch+1),'start %d'%step)
# #    print('train is over')
#
#
# # for step,load in enumerate(validation_loader,0):
# #     load=Variable(load)
# #     test = cnn(load)
#
# # for step,load in enumerate(validation_loader,0):
# #     load=Variable(load)
# #     test = cnnnet(load)
#
# endtime = datetime.datetime.now()
# print ((endtime - starttime).seconds)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # coding=utf-8
# from torch.utils.data import Dataset
# import torch
# import torch.nn as nn
# from torch.autograd import Variable
# import torch.utils.data as Data
# import torch.nn.functional as F
#
# torch_dataset =torch.rand(100,3,224,224)
# y = torch.rand(100)
# train_data = Data.TensorDataset(torch_dataset,y)
# teach_dataset =torch.rand(2000,3,224,224)
#
# validation_loader = torch.utils.data.DataLoader(teach_dataset, batch_size=1)
#
# train_loader = Data.DataLoader(
#     dataset=train_data,      # torch TensorDataset format
#     batch_size=20,      # mini batch size
#     shuffle=True,               # random shuffle for training
# )
#
# class Net(nn.Module):
#     def __init__(self):
#         super(Net, self).__init__()
#
#         def conv_bn(inp, oup, stride):
#             return nn.Sequential(
#                 nn.Conv2d(inp, oup, 3, stride, 1, bias=False),
#                 nn.BatchNorm2d(oup),
#                 nn.ReLU(inplace=True)
#             )
#
#         def conv_dw(inp, oup, stride):
#             return nn.Sequential(
#                 nn.Conv2d(inp, inp, 3, stride, 1, groups=inp, bias=False),
#                 nn.BatchNorm2d(inp),
#                 nn.ReLU(inplace=True),
#
#                 nn.Conv2d(inp, oup, 1, 1, 0, bias=False),
#                 nn.BatchNorm2d(oup),
#                 nn.ReLU(inplace=True),
#             )
#
#         self.model = nn.Sequential(
#             conv_bn(3, 32, 2),
#             conv_dw(32, 64, 1),
#             conv_dw(64, 128, 2),
#             conv_dw(128, 128, 1),
#             conv_dw(128, 256, 2),
#             conv_dw(256, 256, 1),
#             conv_dw(256, 512, 2),
#             conv_dw(512, 512, 1),
#             conv_dw(512, 512, 1),
#             conv_dw(512, 512, 1),
#             conv_dw(512, 512, 1),
#             conv_dw(512, 512, 1),
#             conv_dw(512, 1024, 2),
#             conv_dw(1024, 1024, 1),
#             nn.AvgPool2d(7),
#         )
#         self.fc = nn.Linear(1024, 1)
#
#     def forward(self, x):
#         x = self.model(x)
#         x = x.view(-1, 1024)
#         x = self.fc(x)
#         output = F.softmax(x,dim=1)    # import torch.nn.funtional as F
#         return output
#
#
# net = Net()
#
# LR = 0.001              # learning rate
# cnn = Net()
# # print(cnn)  # net architecture
# optimzer = torch.optim.Adam(cnn.parameters(),lr=LR) # define optimezer
# loss_func = nn.CrossEntropyLoss()   # define loss_function 交叉嫡误差
#
# for epoch in range(1):
#     for step,(x,y) in enumerate(train_loader):  # gives batch data
#         b_x = Variable(x)
#         b_y = Variable(y)
#         output = cnn(b_x)   # cnn output
#         # print(output.shape)
#         loss = loss_func(output,b_y.long())    # cross entropy loss
#         # update W
#         optimzer.zero_grad()
#         loss.backward()
#         optimzer.step()
#         print('epoch %d'%(epoch+1),'start %d'%step)
#
#
# def save_net(meet):
#     torch.save(meet, 'net.pkl')  # 保存整个网络
#     torch.save(meet.state_dict(), 'net_params.pkl')  # 只保存网络中的参数 (速度快, 占内存少)
#     print('save_done')
#
#
# save_net(net)
#
#
#
# # f = open("foo.txt", "a")
# # f.write( "Python 是一个非常好的语言。\n是的，的确非常好!!\n" )
# # f.close()


#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # coding=utf-8
# import os
# import torch.optim as optim
# from torch.utils.data import Dataset
# import datetime
# from support import *
# from mobilenetv1 import *
# from mobilenetv2 import *
#
#
# # 训练参数参数
# epochs = 5 # 训练次数
# batch_size = 1  # 批处理大小
# num_workers = 0  # 多线程的数目
# LR=0.001
#
#
# # kaggle原始数据集地址
# # original_dataset_dir = r'sdsds\train'
# original_dataset_dir = r'C:\Users\Yuki\Desktop\bugs\python\graduation_design\New folder\train'
# total_num = int(len(os.listdir(original_dataset_dir)) / 2)
# random_idx = np.array(range(total_num))
# np.random.shuffle(random_idx)
# print(total_num)
#
#
# # 对加载的图像作归一化处理， 并裁剪为[224x224x3]大小的图像
# data_transform=datatransform()
#
#
# #加载数据
# train_dataset = datasets.ImageFolder(root=r'C:\Users\Yuki\Desktop\bugs\python\graduation_design\New folder\train',
#                                      transform=data_transform)
# # train_dataset = datasets.ImageFolder(root=r'sdsds\train',
# #                                      transform=data_transform)
# train_loader = torch.utils.data.DataLoader(train_dataset,
#                                            batch_size=batch_size,
#                                            shuffle=True,
#                                            num_workers=num_workers)
# test_dataset = datasets.ImageFolder(root=r'C:\Users\Yuki\Desktop\bugs\python\graduation_design\New folder\test', transform=data_transform)
# # test_dataset = datasets.ImageFolder(root=r'sdsds\test', transform=data_transform)
# test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
#
#
# #网络实例化
# net = mobilenetv2(num_classes=2)
# print(net)
#
#
# # 定义loss和optimizer
# cirterion = nn.CrossEntropyLoss()
# optimizer = optim.SGD(net.parameters(), lr=LR, momentum=0.9)
#
#
# def train(LR):
#     for epoch in range(epochs):
#         starttime = datetime.datetime.now()
#         running_loss = 0.0
#         train_correct = 0
#         train_total = 0
#         # print("yes\n")
#         for i, data in enumerate(train_loader, 0):
#             inputs, train_labels = data
#             inputs, labels = Variable(inputs), Variable(train_labels)
#             optimizer.zero_grad()
#             outputs = net(inputs)
#             _, train_predicted = torch.max(outputs.data, 1)
#             train_correct += (train_predicted == labels.data).sum()
#             loss = cirterion(outputs, labels)
#             loss.backward()
#             optimizer.step()
#             running_loss += loss.item()
#             train_total += train_labels.size(0)
#             # print("%d\n"%(i))
#         endtime = datetime.datetime.now()
#         loadingtime=(endtime - starttime).seconds
#         # print(loadingtime)
#         # print('train %d epoch loss: %.3f  acc: %.3f  load:%d' % (
#         #     epoch + 1, running_loss / train_total, 100 * train_correct / train_total,loadingtime))
#         # f = open("foo.txt", "a")
#         # f.write('train %d epoch loss: %.3f  acc: %.3f  load:%d \n' % (
#         #     epoch + 1, running_loss / train_total, 100 * train_correct / train_total,loadingtime))
#         # f.close()
#         # 模型测试
#         correct = 0
#         test_loss = 0.0
#         test_total = 0
#         net.eval()
#         for data in test_loader:
#             images, labels = data
#             images, labels = Variable(images), Variable(labels)
#             outputs = net(images)
#             _, predicted = torch.max(outputs.data, 1)
#             loss = cirterion(outputs, labels)
#             test_loss += loss.item()
#             test_total += labels.size(0)
#             correct += (predicted == labels.data).sum()
#         endtime2 = datetime.datetime.now()
#         loadingtime2=(endtime2 - endtime).seconds
        # print(loadingtime2)
        # print('test  %d epoch loss: %.3f  acc: %.3f ' % (epoch + 1, test_loss / test_total, 100 * correct / test_total))
        # f = open("foo.txt", "a")
        # f.write('test  %d epoch loss: %.3f  acc: %.3f  load:%d\n' % (epoch + 1, test_loss / test_total, 100 * correct / test_total,loadingtime2))
        # f.close()
#         if epoch == 2:
#             LR=LR/10
#             print(LR)
#         if epoch == 4:
#             LR=LR/10
#             print(LR)
#
#
# train(LR)
#
#
# restore_net(net)
#
#
# a = 10
# def test(a):
#     for x in range(5) :
#         if x==3:
#             a=20
#         print(a)
# test(a)


import torch
import torch.nn as nn
import torch.nn.functional as F


class LinearBottleNeck(nn.Module):

    def __init__(self, in_channels, out_channels, stride, t=6, class_num=100):
        super().__init__()

        self.residual = nn.Sequential(
            nn.Conv2d(in_channels, in_channels * t, 1),
            nn.BatchNorm2d(in_channels * t),
            nn.ReLU6(inplace=True),

            nn.Conv2d(in_channels * t, in_channels * t, 3, stride=stride, padding=1, groups=in_channels * t),
            nn.BatchNorm2d(in_channels * t),
            nn.ReLU6(inplace=True),

            nn.Conv2d(in_channels * t, out_channels, 1),
            nn.BatchNorm2d(out_channels)
        )

        self.stride = stride
        self.in_channels = in_channels
        self.out_channels = out_channels

    def forward(self, x):
        residual = self.residual(x)

        if self.stride == 1 and self.in_channels == self.out_channels:
            residual += x

        return residual


class MobileNetV2(nn.Module):

    def __init__(self, class_num=100):
        super().__init__()

        self.pre = nn.Sequential(
            nn.Conv2d(3, 32, 2, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU6(inplace=True)
        )

        self.stage1 = LinearBottleNeck(32, 16, 1, 1)
        self.stage2 = self._make_stage(2, 16, 24, 2, 6)
        self.stage3 = self._make_stage(3, 24, 32, 2, 6)
        self.stage4 = self._make_stage(4, 32, 64, 2, 6)
        self.stage5 = self._make_stage(3, 64, 96, 1, 6)
        self.stage6 = self._make_stage(3, 96, 160, 1, 6)
        self.stage7 = LinearBottleNeck(160, 320, 1, 6)

        self.conv1 = nn.Sequential(
            nn.Conv2d(320, 1280, 1),
            nn.BatchNorm2d(1280),
            nn.ReLU6(inplace=True)
        )

        self.conv2 = nn.Conv2d(1280, class_num, 1)

    def forward(self, x):
        x = self.pre(x)
        x = self.stage1(x)
        x = self.stage2(x)
        x = self.stage3(x)
        x = self.stage4(x)
        x = self.stage5(x)
        x = self.stage6(x)
        x = self.stage7(x)
        x = self.conv1(x)
        x = F.adaptive_avg_pool2d(x, 1)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)

        return x

    def _make_stage(self, repeat, in_channels, out_channels, stride, t):
        layers = []
        layers.append(LinearBottleNeck(in_channels, out_channels, stride, t))

        while repeat - 1:
            layers.append(LinearBottleNeck(out_channels, out_channels, 1, t))
            repeat -= 1

        return nn.Sequential(*layers)


def mobilenetv2():
    return MobileNetV2()




