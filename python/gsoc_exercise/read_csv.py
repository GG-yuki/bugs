import numpy as np
import csv
import matplotlib.pyplot as plt


def load_train_data(root):
    la = []
    with open(root) as file:
        lines = csv.reader(file)
        for line in lines:
            la.append(line)
    la = np.array(la)
    return to_int(la)


def to_int(array):
    array = np.mat(array)
    m, n = np.shape(array)
    newarray = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            newarray[i, j] = float(array[i, j])
    return newarray


data1 = load_train_data(r'./Moon/Albedo_Map.csv')
data1 = data1.reshape(1, -1)
print(len(data1[0]))
data1 = data1[0]

data2 = load_train_data(r'./Moon/LPFe_Map.csv')
data2 = data2.reshape(1, -1)
print(len(data2[0]))
data2 = data2[0]

plt.plot(data1, data2)
plt.show()
