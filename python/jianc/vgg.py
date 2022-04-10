import os
import torch
from torchvision import transforms, datasets
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


class VGG(nn.Module):

    def __init__(self, features, num_classes=2, init_weights=True):
        super(VGG, self).__init__()
        self.features = features
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(True),
            nn.Dropout(0.2),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Dropout(0.2),
            nn.Linear(4096, num_classes),
        )
        if init_weights:
            self._initialize_weights()

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        output = self.classifier(x)
        return output

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
                if m.bias is not None:
                    m.bias.data.zero_()
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.Linear):
                m.weight.data.normal_(0, 0.01)
                m.bias.data.zero_()


def make_layers(cfg, batch_norm=False):
    layers = []
    in_channels = 3
    for v in cfg:
        if v == 'M':
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        else:
            conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1)
            if batch_norm:
                layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
            else:
                layers += [conv2d, nn.ReLU(inplace=True)]
            in_channels = v
    return nn.Sequential(*layers)


cfg = {
    'A': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'B': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'D': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
    'E': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M'],
}



def vgg16(**kwargs):
    model = VGG(make_layers(cfg['E']), **kwargs)
    return model


data_transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

data_transform1 = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


if __name__ == '__main__':

    train_dataset = MyDataSet('/media/dennis/ubuntu/ship_classification/data/final/train/label.txt', data_transform)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=8, shuffle=True, num_workers=4)

    test_dataset = MyDataSet('/media/dennis/ubuntu/ship_classification/data/final/test/label.txt', data_transform)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1, shuffle=True, num_workers=4)

    net = vgg16().cuda()
    print(net)

    cirterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.005, momentum=0.9)

    correct = 0
    total = 0

    for epoch in range(200):
        running_loss = 0.0
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data
            inputs, labels = inputs.cuda(), labels.cuda()
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
                print('[%d %5d] train_loss: %.3f train_ACC:%d %%' % (epoch + 1, i + 1, running_loss / 100, 100 * correct / total))
                running_loss = 0.0
        
        if epoch % 10 == 0:
            start = time.time()
            correct_test = 0
            total_test = 0
            for data in test_loader:
                images, labels = data
                images, labels = images.cuda(), labels.cuda()
                outputs = net(images)

                predicted = torch.max(outputs.data, 1)[1]
                total_test += labels.size(0)
                correct_test += (predicted == labels).sum()
            end = time.time()
            timeuse = end - start

            print('Accuracy of the network on the test images: %d %%, time are %f s' % ((100 * correct_test / total_test), timeuse))
    torch.save(net.state_dict(), 'vgg16_net_paramters.pkl')
    print('finished training!')

