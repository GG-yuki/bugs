import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

y1 = [0.136605972, 0.136469277, 0.130889315, 0.133313604, 0.11909372, 0.121705408, 0.11358577, 0.114529183]
y2 = [0.365347048, 0.357440034, 0.34394093, 0.341293495, 0.280585296, 0.274198419, 0.241980423, 0.235863937]
x1 = [10, 15, 20, 25, 50, 75, 100, 138]
IC1 = 13.53
t1 = 0.1631
b1 = 0.1101
z1 = []
z2 = []
for y in y1:
    z = IC1 * (t1 - b1) / (y - b1) - IC1
    z1.append(z)
print(z1)
IC2 = 16.46
t2 = 0.4927
b2 = 0.212
for y in y2:
    z = IC2 * (t2 - b2) / (y - b2) - IC2
    z2.append(z)
print(z2)


