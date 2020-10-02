#!/usr/bin/python
from scipy.spatial.distance import pdist, squareform, euclidean
import numpy as np

from Cal_Formula import Cal_Pruning_Threshold as C_P_T
from Cal_Formula import Cal_Class_Contribution as C_C_C

# KNN-MODEL-PRUNING

# Knn_Model_Pruning
# @param traningSetS list
# @param traningSetZFile string
# return new_traning_set_S list
def Knn_Model_Pruning(traningSetS, traningSetZFile):


    # Step 1 ~ 4:
    # Get Pruning Threshold of Traning Set S.
    W_S, W_SX = C_P_T.Cal_Pruning_Threshold_By_Data(traningSetS)
    # Get Pruning Threshold of Traning Set Z1.
    W_Z, W_ZX = C_P_T.Cal_Pruning_Threshold_By_File(traningSetZFile)

    # get data to pruning.
    # dataS = np.genfromtxt(traningSetS, delimiter=" ", skip_header=False)
    dataS = traningSetS
    dataZ = np.genfromtxt(traningSetZFile, delimiter=" ", skip_header=False)

    # print W_SX
    print len(dataS)
    new_traning_set_S = []

    # Step 5:
    # Reduce Traning Set S.
    for i, W_X in enumerate(W_SX):
        if W_X > W_S:
            new_traning_set_S.append(dataS[i])

    print len(new_traning_set_S)

    # Step 6:
    # Add Traning Set S.
    for i, W_X in enumerate(W_ZX):
        if W_X > W_Z:
            new_traning_set_S.append(dataZ[i])

    print len(new_traning_set_S)


    return new_traning_set_S
    
    # np.savetxt("new_traning_set_S.txt", new_traning_set_S, fmt='%.8f')



