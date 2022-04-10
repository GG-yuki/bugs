import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 创建函数，用于生成不同属于一个平面的100个离散点
x = [13.523903173216974, 13.664147188790954, 20.96319999239993, 17.3609379172661, 66.2023020952398, 48.2592968519504, 192.18925284800778, 148.3711903549705]
y = [13.669839864931738, 15.307883112568586, 18.558109998163587, 19.275146613524534, 50.90607216800526, 57.82359232089161, 137.65130123147364, 177.1510542028334]
z = [10, 15, 20, 25, 50, 75, 100, 138]
# 创建系数矩阵A
a = 0
A = np.ones((8, 3))
for i in range(0, 8):
    A[i, 0] = x[a]
    A[i, 1] = y[a]
    a = a + 1
# print(A)

# 创建矩阵b
b = np.zeros((8, 1))
a = 0
for i in range(0, 8):
    b[i, 0] = z[a]
    a = a + 1
# print(b)

# 通过X=(AT*A)-1*AT*b直接求解
A_T = A.T
A1 = np.dot(A_T, A)
A2 = np.linalg.inv(A1)
A3 = np.dot(A2, A_T)
X = np.dot(A3, b)
print('平面拟合结果为：z = %.3f * x + %.3f * y + %.3f' % (X[0, 0], X[1, 0], X[2, 0]))

# 计算方差
R = 0
for i in range(0, 8):
    R = R + (X[0, 0] * x[i] + X[1, 0] * y[i] + X[2, 0] - z[i]) ** 2
print('方差为：%.*f' % (3, R))

# 展示图像
fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_zlabel("z")
ax1.scatter(x, y, z, c='r', marker='o')
x_p = np.linspace(0, 300, 100)
y_p = np.linspace(0, 300, 100)
x_p, y_p = np.meshgrid(x_p, y_p)
z_p = X[0, 0] * x_p + X[1, 0] * y_p + X[2, 0]
ax1.plot_wireframe(x_p, y_p, z_p, rstride=10, cstride=10)
plt.show()
