import os
from skimage import io
import torchvision as tv
import numpy as np

root = r'./dataset'
character_train = [[] for i in range(10)]
character_test = [[] for i in range(10)]

<<<<<<< HEAD
train_set = tv.datasets.CIFAR10(r'./dataset', train=True, download=False)
test_set = tv.datasets.CIFAR10(r'./dataset', train=False, download=False)
=======
train_set = tv.datasets.CIFAR10(r'./dataset', train=True, download=True)
# test_set = tv.datasets.CIFAR10(r'./dataset', train=False, download=True)
>>>>>>> a240ef68 (first commit)
#
trainset = []
testset = []

for i, (X, Y) in enumerate(train_set):  # 将train_set的数据和label读入列表
<<<<<<< HEAD
    trainset.append(list((np.array(X), np.array(Y))))
for i, (X, Y) in enumerate(test_set):  # 将test_set的数据和label读入列表
    testset.append(list((np.array(X), np.array(Y))))
=======
    if i < 50:
        trainset.append(list((np.array(X), np.array(Y))))
# for i, (X, Y) in enumerate(test_set):  # 将test_set的数据和label读入列表
#     testset.append(list((np.array(X), np.array(Y))))
>>>>>>> a240ef68 (first commit)


for X, Y in trainset:
    character_train[Y].append(X)  # 32*32*3

<<<<<<< HEAD
for X, Y in testset:
    character_test[Y].append(X)  # 32*32*3

os.mkdir(os.path.join(root, 'train'))
os.mkdir(os.path.join(root, 'test'))

for i, per_class in enumerate(character_train):
    character_path = os.path.join(root, 'train', 'character_' + str(i))
=======
# for X, Y in testset:
#     character_test[Y].append(X)  # 32*32*3

# os.mkdir(os.path.join(root, '50_train'))
# os.mkdir(os.path.join(root, 'test'))

for i, per_class in enumerate(character_train):
    character_path = os.path.join(root, '50_train', 'character_' + str(i))
>>>>>>> a240ef68 (first commit)
    os.mkdir(character_path)
    for j, img in enumerate(per_class):
        img_path = character_path + '/' + str(j) + ".jpg"
        io.imsave(img_path, img)

<<<<<<< HEAD
for i, per_class in enumerate(character_test):
    character_path = os.path.join(root, 'test', 'character_' + str(i))
    os.mkdir(character_path)
    for j, img in enumerate(per_class):
        img_path = character_path + '/' + str(j) + ".jpg"
        io.imsave(img_path, img)
=======
# for i, per_class in enumerate(character_test):
#     character_path = os.path.join(root, 'test', 'character_' + str(i))
#     os.mkdir(character_path)
#     for j, img in enumerate(per_class):
#         img_path = character_path + '/' + str(j) + ".jpg"
#         io.imsave(img_path, img)
>>>>>>> a240ef68 (first commit)
