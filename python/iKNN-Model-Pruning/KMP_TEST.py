#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import os
import numpy as np


from Cal_Formula import Knn_Model_Pruning as K_M_P


def main():

    # 获取原数据集 S 路径
    if os.path.isfile(sys.argv[1]) == False:
        print '找不到原训练集 S，请核对路径后重试'
        sys.exit(-1)
    
    # 初始化新训练集 S
    new_traning_set_S = np.genfromtxt(sys.argv[1], delimiter=" ", skip_header=False)
    old_traning_set_len = len(new_traning_set_S)


    # 从增量数据集 z 开始修剪
    for i, argv in enumerate(sys.argv[2:-1]):
        # 找不到增量数据集 z
        if os.path.isfile(argv) == False:
            print '找不到增量数据集 Z',i+1,':',argv,'，请核对路径后重试'
            print '新数据集剪枝已经进行了',i,'次'
            np.savetxt(sys.argv[-1], new_traning_set_S, fmt='%.8f')
            sys.exit(-1)
        # 进行训练集修剪
        else:
            new_traning_set_S = K_M_P.Knn_Model_Pruning(new_traning_set_S, argv)
    
    # 剪枝执行完毕
    new_traning_set_len = len(new_traning_set_S)
    print '数据剪枝完成'
    print 'new -->', new_traning_set_len
    print 'old -->', old_traning_set_len
    print '剪枝完成度s ＝ ', (100* new_traning_set_len)/old_traning_set_len,'%'
    np.savetxt(sys.argv[-1], new_traning_set_S, fmt='%.8f')
    



if __name__ == '__main__':
    main()