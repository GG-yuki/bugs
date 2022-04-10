#  最小二乘法
import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 4, 5], dtype=np.float64)
y = np.array([1, 3.0, 2, 3, 5])
plt.scatter(x, y)

x_mean = np.mean(x)
y_mean = np.mean(y)
num = 0.0
d = 0.0
a = 0.0
b = 0.0

#  算法主要部分，可尝试自己推导后编写
for x_i, y_i in zip(x, y):
    num += (x_i - x_mean) * (y_i - y_mean)
    d += (x_i - x_mean) ** 2
a = num / d
b = y_mean - a * x_mean
y_hat = a * x + b

plt.figure(2)
plt.scatter(x, y)
plt.plot(x, y_hat, c='r')
x_predict = 4.8
y_predict = a * x_predict + b
print(y_predict)
plt.scatter(x_predict, y_predict, c='b', marker='+')
plt.show()
