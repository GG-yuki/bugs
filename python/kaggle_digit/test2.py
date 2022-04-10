import numpy as np
import csv
import operator

def saveResult(result):
    n=1
    with open('result.csv','w',newline='')  as myFile:
        myWriter=csv.writer(myFile)
        myWriter.writerows([['ImageId','Label']])
        for i in result:
            tmp=[]
            tmp.append([n,i])
            n=n+1
            myWriter.writerows(tmp)

Result=[]
Result.append(2)
Result.append(3)

saveResult(Result)


