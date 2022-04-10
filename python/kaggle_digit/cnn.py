import numpy as np
import csv
import operator


def loadTrainData():
    l = []
    with open('train.csv') as file:
        lines = csv.reader(file)
        for line in lines:
            l.append(line)  # 42001*785
    l.remove(l[0])
    l = np.array(l)
    label = l[:, 0]
    data = l[:, 1:]
    return nomalizing(toInt(data)), toInt(label)


def toInt(array):
    array = np.mat(array)
    m, n = np.shape(array)
    newArray = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            newArray[i, j] = int(array[i, j])
    return newArray


def nomalizing(array):
    m, n = np.shape(array)
    for i in range(m):
        for j in range(n):
            if array[i, j] != 0:
                array[i, j] = 1
    return array


def loadTestData():
    l = []
    with open('test.csv') as file:
        lines = csv.reader(file)
        for line in lines:
            l.append(line)
    # 28001*784
    l.remove(l[0])
    data = np.array(l)
    return nomalizing(toInt(data))


def loadTestResult():
    l = []
    with open('cnn_mnist_datagen.csv') as file:
        lines = csv.reader(file)
        for line in lines:
            l.append(line)
    # 28001*2
    l.remove(l[0])
    label = np.array(l)
    return toInt(label[:, 1])


def classify(inX, dataSet, labels, k):
    inX = np.mat(inX)
    dataSet = np.mat(dataSet)
    labels = np.mat(labels)
    dataSetSize = dataSet.shape[0]
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = (np.array(diffMat)) ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[0, sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def saveResult(result):
    n = 1
    with open('result.csv', 'w', newline='') as myFile:
        myWriter = csv.writer(myFile)
        myWriter.writerows([['ImageId', 'Label']])
        for i in result:
            tmp = []
            tmp.append([n, i])
            n = n + 1
            myWriter.writerows(tmp)


def handwritingClassTest():
    trainData, trainLabel = loadTrainData()
    testData = loadTestData()
    testLabel = loadTestResult()
    m, n = np.shape(testData)
    errorCount = 0
    resultList = []
    for i in range(m):
        classifierResult = classify(testData[i], trainData, trainLabel, 5)
        resultList.append(classifierResult)
        print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, testLabel[0, i]))
        if (classifierResult != testLabel[0, i]): errorCount += 1.0
    print("\nthe total number of errors is: %d" % errorCount)
    print("\nthe total error rate is: %f" % (errorCount / float(m)))
    saveResult(resultList)


handwritingClassTest()
