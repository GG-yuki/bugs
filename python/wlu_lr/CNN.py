import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy

x = torch.unsqueeze(torch.linspace(-1, 1, 300), dim=1)  # x data (tensor), shape=(100, 1)
print(x)
y = x.pow(2) + 0.2 * torch.rand(x.size())  # noisy y data (tensor), shape=(100, 1)
plt.scatter(x.data.numpy(), y.data.numpy())
plt.show()
# print(x[1])
# print(y)

x = [[13.523903173216974], [13.664147188790954], [20.96319999239993], [17.3609379172661], [66.2023020952398],
     [48.2592968519504], [192.18925284800778], [148.3711903549705]]
y = [[13.669839864931738], [15.307883112568586], [18.558109998163587], [19.275146613524534], [50.90607216800526],
     [57.82359232089161], [137.65130123147364], [177.1510542028334]]
z = [[10], [15], [20], [25], [50], [75], [100], [138]]
x = torch.tensor(x)
y = torch.tensor(y)
plt.scatter(x.data.numpy(), y.data.numpy())
plt.show()
# print(x)
# plt.scatter(x.data.numpy(), y.data.numpy())
# plt.show()
# print(x[1])


# # 画图
# plt.scatter(x.data.numpy(), y.data.numpy())
# plt.show()
#
#
class Net(torch.nn.Module):  # 继承 torch 的 Module
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()  # 继承 __init__ 功能
        # 定义每层用什么样的形式
        self.hidden = torch.nn.Linear(n_feature, n_hidden)  # 隐藏层线性输出
        self.predict = torch.nn.Linear(n_hidden, n_output)  # 输出层线性输出

    def forward(self, x1):  # 这同时也是 Module 中的 forward 功能
        # 正向传播输入值, 神经网络分析出输出值
        x1 = F.relu(self.hidden(x1))  # 激励函数(隐藏层的线性值)
        x1 = self.predict(x1)  # 输出值
        return x1


net = Net(n_feature=1, n_hidden=10, n_output=1)

# plt.ion()   # 画图
# plt.show()
# # optimizer 是训练的工具
optimizer = torch.optim.SGD(net.parameters(), lr=0.2)  # 传入 net 的所有参数, 学习率
loss_func = torch.nn.MSELoss()  # 预测值和真实值的误差计算公式 (均方差)

for t in range(100):
    prediction = net(x)  # 喂给 net 训练数据 x, 输出预测值
    print(prediction)
    loss = loss_func(prediction, y)  # 计算两者的误差

    optimizer.zero_grad()  # 清空上一步的残余更新参数值
    loss.backward()  # 误差反向传播, 计算参数更新值
    optimizer.step()  # 将参数更新值施加到 net 的 parameters 上

    if t % 5 == 0:
        # plot and show learning process
        plt.cla()
        plt.scatter(x.data.numpy(), y.data.numpy())
        plt.plot(x.data.numpy(), prediction.data.numpy(), 'r-', lw=5)
        plt.text(0.5, 0, 'Loss=%.4f' % loss.data.numpy(), fontdict={'size': 20, 'color':  'red'})
        plt.pause(0.1)


# y_as = net(x)
# plt.cla()
# plt.scatter(x.data.numpy(), y_as.data.numpy())
# plt.plot(x.data.numpy(), y_as.data.numpy(), 'r-', lw=5)
# plt.text(0.5, 0, 'Loss=%.4f' % loss.data.numpy(), fontdict={'size': 20, 'color':  'red'})
# plt.ion()   # 画图
# plt.show()

