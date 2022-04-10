# coding: utf-8
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms, datasets
import torch


class MyDataset(Dataset):
    def __init__(self, txt_path, transform=None, target_transform=None):
        fh = open(txt_path, 'r')
        imgs = []
        for line in fh:
            line = line.rstrip()
            words = line.split()
            imgs.append((words[0], int(words[1])))
            self.imgs = imgs
            self.transform = transform
            self.target_transform = target_transform

    def __getitem__(self, index):
        fn, label = self.imgs[index]
        img = Image.open(fn).convert('RGB')
        if self.transform is not None:
            img = self.transform(img)
        return img, label, fn

    def __len__(self):
        return len(self.imgs)


class Data_loader_self:

    def __init__(self, root, num_workers, batch_size):
        self.root = root
        self.num_workers = num_workers
        self.batch_size = batch_size
        self.train_transform = train_transform()
        self.test_transform = test_transform()

    def trainloader(self):
        train_dataset = MyDataset(txt_path='./dataset/train.txt', transform=train_transform())
        train_loader = torch.utils.data.DataLoader(train_dataset,
                                                   batch_size=self.batch_size,
                                                   shuffle=True,
                                                   num_workers=self.num_workers)
        return train_loader

    def testloader(self):
        test_dataset = MyDataset(txt_path='./dataset/test.txt', transform=test_transform())
        test_loader = torch.utils.data.DataLoader(test_dataset,
                                                  batch_size=self.batch_size,
                                                  shuffle=True,
                                                  num_workers=self.num_workers)
        return test_loader


def train_transform():
    data_transform = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
    ])
    return data_transform


def test_transform():
    data_transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    return data_transform
