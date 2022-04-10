from support import *
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
import pandas as pd
from mobilenetv1 import *


epochs = 90 # 训练次数
batch_size = 32  # 批处理大小
num_workers = 4 #多线程
LR = 0.001 #初始学习速率


train_path = './ca_leaf_dataset/train_images/'
test_path = './ca_leaf_dataset/test_images/'
train_csv = pd.read_csv('./ca_leaf_dataset/train.csv')
# sample = pd.read_csv('../input/cassava-leaf-disease-classification/sample_submission.csv')


transforms = datatransform()
train_df, val_df = train_test_split(train_csv,test_size=0.2,stratify=train_csv.label)
trainset = MyDataset(train_df, transform=transforms)
train_loader = DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=num_workers)


net = MobileNetV1(5).cuda() # 分类
train(net, epochs, LR, train_loader)