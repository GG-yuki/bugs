import numpy as np
import matplotlib.pyplot as plt
import xlrd
import math
import matplotlib
import matplotlib.font_manager as fm

######################字体大小
font1 = {'family': 'Times New Roman',
         'style': 'normal', 'weight': 'normal',
         'size': 22}
font2 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 27,
         }

w = 4
l = 1.5
s = 25

# ratio value
x = [1, 2, 3, 4, 5]
ra_auc = [0.6632, 0.6609, 0.6741, 0.6809, 0.6756]
ra_f1 = [0.6321, 0.6395, 0.6412, 0.6497, 0.6453]

fig = plt.figure()
ax = plt.subplot(111)

# 折线图的位置及参数调整
ax.plot(x, ra_auc, color='darkorchid', marker='d', markersize=12, label='MobileNetV1', linewidth=w)
ax.plot(x, ra_f1, color='teal', marker='*', markersize=12, label='MobileNetV2', linewidth=w)

ax.legend(loc='lower right', ncol=1, columnspacing=1, handlelength=1, prop=font1, frameon=False)

ax.set_ylim(0.55, 0.70)

fontprop = fm.FontProperties(family='Times New Roman',
                             size=22,
                             weight='normal')

fontprop1 = fm.FontProperties(family='Times New Roman',
                              size=23,
                              weight='normal')

plt.xticks([1, 2, 3, 4, 5], ['0.01', '0.05', '0.1', '0.5', '1'], fontproperties=fontprop1)
plt.yticks([0.60, 0.65, 0.70], fontproperties=fontprop)

ax.set_xlabel('(a) Learning rate(10'+ r'$^-$'+''+r'$^1$'+')', font2)
ax.grid(axis='y', linewidth=1, alpha=0.4)

fig.tight_layout()  # 避免子图重叠
plt.savefig('fig4.jpg')
plt.show()
