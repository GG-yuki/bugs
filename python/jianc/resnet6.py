import os
import torch
from torchvision import transforms, datasets
import torchvision
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import torch.optim as optim
from PIL import Image
import math
import time


class MyDataSet(Dataset):
    def __init__(self, txtPath, data_transform):
        self.imgPathArr = []
        self.labelArr = []
        with open(txtPath, "rb") as f:
            txtArr = f.readlines()
        for i in txtArr:
            fileArr = str(i.strip(), encoding="utf-8").split(" ")
            self.imgPathArr.append(fileArr[0])
            self.labelArr.append(fileArr[1])
        self.transforms = data_transform

    def __getitem__(self, index):
        label = np.array(int(self.labelArr[index]))
        img_path = self.imgPathArr[index]
        pil_img = Image.open(img_path).convert('RGB')
        if self.transforms:
            data = self.transforms(pil_img)
        else:
            pil_img = np.asarray(pil_img)
            data = torch.from_numpy(pil_img)
        return data, label

    def __len__(self):
        return len(self.imgPathArr)


class ResidualBlock(nn.Module):
    def __init__(self, inchannel, outchannel, stride=1):
        super(ResidualBlock, self).__init__()
        self.left = nn.Sequential(
            nn.Conv2d(inchannel, outchannel, kernel_size=3, stride=stride, padding=1, bias=False),
            nn.BatchNorm2d(outchannel),
            nn.ReLU(inplace=True),
            nn.Conv2d(outchannel, outchannel, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(outchannel)
        )
        self.shortcut = nn.Sequential()
        if stride != 1 or inchannel != outchannel:
            self.shortcut = nn.Sequential(
                nn.Conv2d(inchannel, outchannel, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(outchannel)
            )

    def forward(self, x):
        out = self.left(x)
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class ResNet(nn.Module):
    def __init__(self, ResidualBlock, num_classes=2):
        super(ResNet, self).__init__()
        self.inchannel = 64
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(),
        )
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        # self.layer1 = self.make_layer(ResidualBlock, 64, 2, stride=1)
        # self.layer2 = self.make_layer(ResidualBlock, 128, 2, stride=2)
        # self.layer3 = self.make_layer(ResidualBlock, 256, 2, stride=2)
        self.layer4 = self.make_layer(ResidualBlock, 512, 2, stride=2)
        self.avgpool = nn.AdaptiveAvgPool2d(output_size=(1, 1))
        self.fc = nn.Linear(1 * 1 * 512, num_classes)

    def make_layer(self, block, channels, num_blocks, stride):
        strides = [stride] + [1] * (num_blocks - 1)  # strides=[1,1]
        layers = []
        for stride in strides:
            layers.append(block(self.inchannel, channels, stride))
            self.inchannel = channels
        return nn.Sequential(*layers)

    def forward(self, x):
        out = self.conv1(x)
        # print('1:'+str(out.size()))
        out = self.maxpool(out)
        # print('2:'+str(out.size()))
        # out = self.layer1(out)
        # print('1-1:'+str(out.size()))
        # out = self.layer2(out)
        # print('1-2:'+str(out.size()))
        # out = self.layer3(out)
        # print('1-3:'+str(out.size()))
        out = self.layer4(out)
        # print('1-4:'+str(out.size()))
        # out = F.avg_pool2d(out, 4)
        # print('6:'+str(out.size()))
        out = self.avgpool(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out


def ResNet18():
    return ResNet(ResidualBlock)


data_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

if __name__ == '__main__':

    # train_dataset = MyDataSet('/media/dennis/ubuntu/ship_classification/data/final/train/label.txt', data_transform)
    # train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=8, shuffle=True, num_workers=4)
    #
    # test_dataset = MyDataSet('/media/dennis/ubuntu/ship_classification/data/final/test/label.txt', data_transform)
    # test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1, shuffle=True, num_workers=4)

    train_dataset = datasets.ImageFolder(root=r'/home/zhangyunke/jiqiwei/jianc/final/final/train',
                                         transform=data_transform)
    train_loader = torch.utils.data.DataLoader(train_dataset,
                                               batch_size=8,
                                               shuffle=True,
                                               num_workers=4)

    test_dataset = datasets.ImageFolder(root=r'/home/zhangyunke/jiqiwei/jianc/final/final/test',
                                        transform=data_transform)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1, shuffle=True,
                                              num_workers=4)

    net = ResNet18().cuda()
    # net = torchvision.models.resnet18(pretrained=False)
    # num_fc_ftr = net.fc.in_features
    # net.fc = torch.nn.Linear(num_fc_ftr, 2)
    print(net)

    LR = 0.005
    cirterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=LR, momentum=0.9)

    correct = 0
    total = 0

    # net.load_state_dict(torch.load('resnet18_net_paramters.pkl'))

    for epoch in range(200):
        running_loss = 0.0
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data
            inputs, labels = inputs.cuda(), labels.cuda().long()
            outputs = net(inputs)
            loss = cirterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            # if epoch >= 100:
            #     LR = 0.001
            optimizer.step()

            running_loss += loss.item()
            predicted = torch.max(outputs.data, 1)[1]
            total += labels.size(0)
            correct += (predicted == labels).sum()

            if i % 10 == 9:
                print('[%d %5d] train_loss: %.3f train_ACC:%d %%' % (
                epoch + 1, i + 1, running_loss / 100, 100 * correct // total))
                running_loss = 0.0

        if epoch % 10 == 0:
            start = time.time()
            correct_test = 0
            total_test = 0
            for data in test_loader:
                images, labels = data
                images, labels = images.cuda(), labels.cuda()
                net = net.eval()
                outputs = net(images)
                predicted = torch.max(outputs.data, 1)[1]
                # if (predicted[0] < 3):
                #     predicted[0] = 0
                # if (labels[0] < 3):
                #     labels[0] = 0
                total_test += labels.size(0)
                correct_test += (predicted == labels).sum()
            end = time.time()
            timeuse = end - start

            # print('Accuracy of the network on the test images: %d %%, time are %f s' % ((100 * correct_test / total_test), timeuse))
            print('Accuracy of the network on the test images: %d %%, time are %f s' % (
            (100 * correct_test // total_test), timeuse))
            f = open("foo.txt", "a")
            f.write('test  %d epoch, acc: %d %%,  load:%f\n' % (epoch + 1, 100 * correct_test // total_test, timeuse))
            f.close()

    torch.save(net.state_dict(), 'resnet18_net_paramters.pkl')
    print('finished training!')
