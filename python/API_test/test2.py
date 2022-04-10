import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
global update
img = np.array(Image.open('1.jpg'))
im = plt.imshow(img, animated=True)
def update_data():
    return np.array(Image.open('1.jpg'))
plt.imshow(img, animated=True).set_array(update_data())
print(plt.imshow.__defaults__)#使用__code__#总参数个数

print(plt.imshow.__code__.co_argcount)#总参数名

print(plt.imshow.__code__.co_varnames)
