import os
import zipfile

import numpy as np
from PIL import Image
from PIL import ImageFile
import torchvision
import torch
import torch.utils.data as data
from torch.autograd import Variable
from torchvision import transforms


class RMBDataset(data.Dataset):
    def __init__(self, data_dir, transform=None):
        """
        rmb面额分类任务的Dataset
        :param data_dir: str, 数据集所在路径
        :param transform: torch.transform，数据预处理
        """
        self.label_name = {"1": 0, "100": 1}
        self.data_info = self.get_img_info(data_dir)  # data_info存储所有图片路径和标签，在DataLoader中通过index读取样本
        self.transform = transform

    def __getitem__(self, index):

        path_img, label = self.data_info[index]  # 索引读取图像路径和标签
        img = Image.open(path_img).convert('RGB')  # 读取图像，返回Image 类型 0~255

        if self.transform is not None:
            img = self.transform(img)  # 在这里做transform，把图像转为tensor等等

        return img, label

    def __len__(self):
        return len(self.data_info)

    @staticmethod
    def get_img_info(data_dir):
        data_info = list()
        for root, dirs, _ in os.walk(data_dir):
            # 遍历类别
            for sub_dir in dirs:
                img_names = os.listdir(os.path.join(root, sub_dir))
                img_names = list(filter(lambda x: x.endswith('.jpg'), img_names))

                # 遍历图片
                for i in range(len(img_names)):
                    img_name = img_names[i]
                    path_img = os.path.join(root, sub_dir, img_name)
                    label = sub_dir
                    print(sub_dir)
                    data_info.append((path_img, label))
                    print(data_info)

        return data_info  # 返回的也就是图像路径 和 标签

def transform():
    data_transform = transforms.Compose([
        transforms.Resize(8),
        transforms.CenterCrop(8),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return data_transform

# a = RMBDataset(r'./dataset/')

a = torchvision.datasets.ImageFolder(root=r'./dataset', transform=transform())

print(a.subset_indexes)

loader = torch.utils.data.DataLoader(
    a,
    batch_size=2,
    num_workers=1,
    pin_memory=True,
)

for ax, b in enumerate(loader, 0):

    inputs, train_labels = b
    inputs, train_labels = Variable(inputs), Variable(train_labels)

    # print(inputs)

    # print(train_labels)
