import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.utils.data as Data
import matplotlib.pyplot as plt
import torch.nn.functional as F
import csv
import os
from torchvision import datasets,transforms, models

lr=10
for i in range (10):
    print(i,lr)
    if (i+1) % 5 == 0:
        lr = lr/10