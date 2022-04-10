import numpy as np
import matplotlib.pylab as plt

def step_function1(x=''):
    '''
    简单的阶跃函数——无法接收numpy数组参数
    '''
    if x >0:
        return 1
    else:
        return 0

def step_function2(x):
    '''
    升级版的阶跃函数，这里的参数ｘ为numpy数组
    '''
    y = x > 0  # numpy数组中的每个元素都与0比较大小，得到一个布尔型numpy数组
    return y.astype(np.int)   #　astype()方法将numpy数组的布尔型转换为int型

m = 1
print(step_function1(m))

x = np.arange(-5.0,5.0,0.1)  # 生成一个numpy数组，范围是(-5.0,5.0),步长为0.1
y = step_function2(x)
plt.plot(x,y)
plt.ylim(-0.1,1.1)
plt.show()



import numpy as np
import matplotlib.pylab as plt

x1 = np.arange(-5.0, 0, 0.1)  # 生成一个numpy数组，范围是(-5.0,5.0),步长为0.1
y1 = []
for i in range(50):
    y1.append(0)
x1 = np.append(x1, np.arange(0, 1, 0.1))
y1 = np.append(y1, np.arange(0, 1, 0.1))
x1 = np.append(x1, np.arange(1, 5, 0.1))
for i in range(40):
    y1 = np.append(y1,1)
print(y1[52])
plt.plot(x1, y1)
plt.ylim(-0.1, 1.1)
plt.show()


import numpy as np
import matplotlib.pyplot as plt
from scipy import special

x = np.linspace(-10, 10, 100)

y = np.tanh(x)  # tanh函数
# z = special.expit(x)  # sigmoid函数

plt.figure
plt.plot(x, y, color="red", linewidth=2, label="tanh")
# plt.plot(x, z, color="b", linewidth=2, label="sigmoid")
plt.xlabel("abscissa")
plt.ylabel("ordinate")
plt.legend(loc='upper left')
plt.title("tanh&sigmoid Example")
plt.show()
