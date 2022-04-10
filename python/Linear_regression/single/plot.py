#  梯度下降法，直观图

import matplotlib.pyplot as plt
import numpy as np


# fx的函数值
def fx(x):
    return x ** 2


# 定义梯度下降算法
def gradient_descent():
    times = 10  # 迭代次数
    alpha = 0.1  # 学习率
    x = 10  # 设定x的初始值
    x_axis = np.linspace(-10, 10)  # 设定x轴的坐标系
    fig = plt.figure(1, figsize=(5, 5))  # 设定画布大小
    ax = fig.add_subplot(1, 1, 1)  # 设定画布内只有一个图
    ax.set_xlabel('X', fontsize=14)
    ax.set_ylabel('Y', fontsize=14)
    ax.plot(x_axis, fx(x_axis))  # 作图

    for i in range(times):
        x1 = x
        y1 = fx(x)
        print("第%d次迭代：x=%f，y=%f" % (i + 1, x, y1))
        x = x - alpha * 2 * x
        y = fx(x)
        ax.plot([x1, x], [y1, y], 'ko', lw=1, ls='-', color='coral')
    plt.show()


if __name__ == "__main__":
    gradient_descent()
