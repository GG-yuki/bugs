# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import pickle
import numpy as np
from torch.utils.data.sampler import Sampler
import os
import torch
from alexnet import alexnet
from vgg16 import *
from mobilenetv1_sobel import *


def load_net(path=r'./exp/checkpoint.pth.tar'):
    """Loads model and return it without DataParallel table."""
    if True:
        print(("=> loading checkpoint '{}'".format(path)))
        checkpoint = torch.load(path)

        # size of the top layer
        n = checkpoint['state_dict']['top_layer.bias'].size()

        # build skeleton of the model
        sob = 'sobel.0.weight' in list(checkpoint['state_dict'].keys())
        model = alexnet(sobel=sob, out=int(n[0]))

        # deal with a dataparallel table
        def rename_key(key):
            if not 'module' in key:
                return key
            return ''.join(key.split('.module'))

        checkpoint['state_dict'] = {rename_key(key): val
                                    for key, val
                                    in list(checkpoint['state_dict'].items())}

        # load weights
        model.load_state_dict(checkpoint['state_dict'])
        print("Loaded")
    return model


def load_model(path=r'./exp/checkpoint_mobilenetv1.pth.tar'):
    """Loads model and return it without DataParallel table."""
    if True:
        print(("=> loading checkpoint '{}'".format(path)))
        checkpoint = torch.load(path)

        # size of the top layer
        n = checkpoint['state_dict']['top_layer.bias'].size()

        # build skeleton of the model
        sob = 'sobel.0.weight' in list(checkpoint['state_dict'].keys())
        model = MobileNetV1(sobel=True, num_classes=int(n[0]))

        # deal with a dataparallel table
        def rename_key(key):
            if not 'module' in key:
                return key
            return ''.join(key.split('.module'))

        checkpoint['state_dict'] = {rename_key(key): val
                                    for key, val
                                    in list(checkpoint['state_dict'].items())}

        # load weights
        model.load_state_dict(checkpoint['state_dict'])
        print("Loaded")
    return model


class UnifLabelSampler(Sampler):
    """Samples elements uniformely accross pseudolabels.
        Args:
            N (int): size of returned iterator.
            images_lists: dict of key (target), value (list of data with this target)
    """

    def __init__(self, N, images_lists):
        self.N = N
        self.images_lists = images_lists
        self.indexes = self.generate_indexes_epoch()

    def generate_indexes_epoch(self):
        nmb_non_empty_clusters = 0
        for i in range(len(self.images_lists)):
            if len(self.images_lists[i]) != 0:
                nmb_non_empty_clusters += 1

        size_per_pseudolabel = int(self.N / nmb_non_empty_clusters) + 1
        res = np.array([])

        for i in range(len(self.images_lists)):
            # skip empty clusters
            if len(self.images_lists[i]) == 0:
                continue
            indexes = np.random.choice(
                self.images_lists[i],
                size_per_pseudolabel,
                replace=(len(self.images_lists[i]) <= size_per_pseudolabel)
            )
            res = np.concatenate((res, indexes))

        np.random.shuffle(res)
        res = list(res.astype('int'))
        if len(res) >= self.N:
            return res[:self.N]
        res += res[: (self.N - len(res))]
        return res

    def __iter__(self):
        return iter(self.indexes)

    def __len__(self):
        return len(self.indexes)


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def learning_rate_decay(optimizer, t, lr_0):
    for param_group in optimizer.param_groups:
        lr = lr_0 / np.sqrt(1 + lr_0 * param_group['weight_decay'] * t)
        param_group['lr'] = lr


class Logger():
    """ Class to update every epoch to keep trace of the results
    Methods:
        - log() log and save
    """

    def __init__(self, path):
        self.path = path
        self.data = []

    def log(self, train_point):
        self.data.append(train_point)
        with open(os.path.join(self.path), 'wb') as fp:
            pickle.dump(self.data, fp, -1)


def load_net(net):
    # restore entire net1 to net2
    model_load = torch.load('./pkl/epoch_' + net + '_net.pkl')
    return model_load


def write_result(model, epochs, batch_size, num_workers, lr, max_acc, weight_decay):
    f = open('./experiment_record(first)/' + model + '/final_result.txt', "a")
    f.write('model %s   train %d epoch   batch_size %d   num_workers %d   lr %f   max_acc: %.3f  '
            'weight_decay %f\n' %
            (model, epochs, batch_size, num_workers, lr, max_acc, weight_decay))
    f.close()
