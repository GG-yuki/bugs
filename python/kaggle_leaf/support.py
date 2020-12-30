"""
/********************************************************************
*
*  文件名：support.py
*
*  文件描述：封装类
*
*  创建人： qiwei_ji, 2020年12月6日
*
*  版本号：2.1
*
*  修改记录：65
*
********************************************************************/
"""
import torch
import torch.nn as nn
from torchvision import transforms
import torch.optim as optim
import datetime
import cv2
from torch.utils.data import Dataset
from torch.autograd import Variable
from tqdm import tqdm


class MyDataset(Dataset):

    def __init__(self, dataframe, transform=None, test=False):
        self.df = dataframe
        self.transform = transform
        self.test = test

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):

        label = self.df.label.values[idx]
        p = self.df.image_id.values[idx]
        train_path = './ca_leaf_dataset/train_images/'
        test_path = './ca_leaf_dataset/test_images/'

        if self.test == False:
            p_path = train_path + p
        else:
            p_path = test_path + p

        image = cv2.imread(p_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = transforms.ToPILImage()(image)

        if self.transform:
            image = self.transform(image)

        return image, label


class AverageMeter:
    """
    Computes and stores the average and current value
    """

    def __init__(self):
        self.val = 0
        self.reset()

    def reset(self):
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


# 保存网络
def save_net(net):
    torch.save(net, 'net.pkl')  # 保存整个网络
    torch.save(net.state_dict(), 'net_params.pkl')  # 只保存网络中的参数 (速度快, 占内存少)
    print('save_done')


# 提取网络
def load_net():
    # restore entire net1 to net2
    net = torch.load('net.pkl')
    torch.save(net.state_dict(), 'net_params.pkl')  # 只保存网络中的参数 (速度快, 占内存少)
    return net


# 图像归一化后裁剪，最后尺寸224*224*3
def datatransform():
    data_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return data_transform


# 定义训练过程
def train(net, epochs, LR, train_loader):
    # 定义loss和optimizer
    cirterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=LR, momentum=0.9)
    losses = AverageMeter()
    accs = AverageMeter()

    for epoch in range(epochs):
        starttime = datetime.datetime.now()  # 计时

        # 训练开始
        running_loss = 0.0
        train_correct = 0
        train_total = 0
        print("yes\n")
        tk = tqdm(train_loader, total=len(train_loader), position=0, leave=True)
        for idx, (inputs, labels) in enumerate(tk):
            inputs, labels = inputs.cuda(), labels.cuda().long()
            outputs = net(inputs)

            loss = cirterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            train_total += labels.size(0)
            train_correct += ((outputs.argmax(1) == labels).sum().item())
            losses.update(loss.item(), inputs.size(0))
            accs.update((outputs.argmax(1) == labels).sum().item() / inputs.size(0), inputs.size(0))
            tk.set_postfix(loss=losses.avg, acc=accs.avg)

            # 训练计时
        endtime = datetime.datetime.now()
        loadingtime = (endtime - starttime).seconds

        # 打印训练结果
        print('train %d epoch loss: %.3f  acc: %.3f  load:%d' % (
            epoch + 1, running_loss / train_total, 100 * train_correct / train_total, loadingtime))
        f = open("foo.txt", "a")
        f.write('train %d epoch loss: %.3f  acc: %.3f  load:%d \n' % (
            epoch + 1, running_loss / train_total, 100 * train_correct / train_total, loadingtime))
        f.close()

        if epoch % 30 == 0:
            LR = LR / 10
