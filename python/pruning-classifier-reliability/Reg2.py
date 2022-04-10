import pandas as pd 
import numpy as np 
from sklearn.metrics import accuracy_score
from sklearn import neighbors
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split 
from sklearn import svm
import math
#data = pd.read_csv('KS_original_pre_process.csv')
#data = pd.read_csv('KS_manual_pre_process.csv')
data = pd.read_csv('appstore_grubb.csv')
ogdf = pd.read_csv('appstore_og.csv')
print(data.shape)
columnNames = list(data.head(0))
columnNames.remove('user_rating_ver')
columnNames.remove('user_rating')

print(columnNames)
columns_target = ['user_rating'] 
columns_train = columnNames


X = data[columns_train] 
Y = data[columns_target]
OX = ogdf[columns_train] 
OY = ogdf[columns_target]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state=50)
OX_train, OX_test, OY_train, OY_test = train_test_split(OX, OY, test_size=0.25, random_state=50)

   
from sklearn.model_selection import KFold

kf = KFold(n_splits=10)
kf.get_n_splits(X)
KFold(n_splits=10, random_state= 0, shuffle=False)
print("No of Splits: ", kf.get_n_splits(X))


for train_index, test_index in kf.split(X):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X.iloc[train_index], X.iloc[test_index] 
    Y_train, Y_test = Y.iloc[train_index], Y.iloc[test_index]

for train_index, test_index in kf.split(X):
    print("TRAIN:", train_index, "TEST:", test_index)
    OX_train, OX_test = OX.iloc[train_index], OX.iloc[test_index]
    OY_train, OY_test = OY.iloc[train_index], OY.iloc[test_index]

from sklearn.metrics import mean_absolute_error
for train_index, test_index in kf.split(X):
    rmse = [0,0,0,0]
    mae1 = [0,0,0,0]
    mse = [0,0,0,0]
  
    svm_model=svm.SVR()
    svm_model.fit(X_train, np.ravel(Y_train))
    #print(svm_model.score(OX_test,OY_test))
    pred = svm_model.predict(OX_test)
    p1 = np.ravel(OY_test)
    p2 = np.ravel(pred)
    print(math.sqrt(((p1-p2)**2).mean()))
    print(mean_absolute_error(p1,p2))
    print(((p1-p2)**2).mean())
    rmse[0] = math.sqrt(((p1-p2)**2).mean())
    mae1[0] = mean_absolute_error(p1,p2)
    mse[0] =((p1-p2)**2).mean()

    regression_model = LinearRegression(copy_X=True, fit_intercept=True,n_jobs=None, normalize=False)
    regression_model.fit(X_train, np.ravel(Y_train))
    pred = regression_model.predict(OX_test)
    #print(regression_model.score(OX_test,OY_test))
    #result = pd.DataFrame({'Actual':OY_test,'Predicted':pred})
    p1 = np.ravel(OY_test)
    p2 = np.ravel(pred)
    print(math.sqrt(((p1-p2)**2).mean()))
    print(mean_absolute_error(p1,p2))
    print(((p1-p2)**2).mean())
    rmse[1] = math.sqrt(((p1-p2)**2).mean())
    mae1[1] = mean_absolute_error(p1,p2)
    mse[1] =((p1-p2)**2).mean()


    #print(((OY_test-pred)**2))
    knn_model = KNeighborsRegressor(n_neighbors=15, algorithm='auto', leaf_size=30, metric='minkowski',p=2, weights='uniform')
    knn_model.fit(X_train, np.ravel(Y_train))
    #print(knn_model.score(OX_test,OY_test))
    pred = knn_model.predict(OX_test)
    p1 = np.ravel(OY_test)
    p2 = np.ravel(pred)
    print(math.sqrt(((p1-p2)**2).mean()))
    print(mean_absolute_error(p1,p2))
    print(((p1-p2)**2).mean())
    rmse[2] = math.sqrt(((p1-p2)**2).mean())
    mae1[2] = mean_absolute_error(p1,p2)
    mse[2] =((p1-p2)**2).mean()


    rfr_model = RandomForestRegressor(n_jobs=-1)
    rfr_model.fit(X_train, np.ravel(Y_train))
    #print(rfr_model.score(OX_test,OY_test))
    pred = rfr_model.predict(OX_test)
    p1 = np.ravel(OY_test)
    p2 = np.ravel(pred)
    print(math.sqrt(((p1-p2)**2).mean()))
    print(mean_absolute_error(p1,p2))
    print(((p1-p2)**2).mean())
    rmse[3] = math.sqrt(((p1-p2)**2).mean())
    mae1[3] = mean_absolute_error(p1,p2)
    mse[3] =((p1-p2)**2).mean()


    print("----------------------------")
    print("RMSE ", rmse)
    print("MAE ", mae1)
    print("MSE ", mse)
    
itr = 1

aa = np.array(rmse).reshape(itr,4)
bb = aa.mean(axis=0)
print(aa.mean(axis=0))
fig, ax = plt.subplots()
objects = ('SVM', 'LiR', 'KNN', 'RFR')
y_pos = np.arange(len(objects))
performance = [bb[0],bb[1],bb[2],bb[3]]
bar = plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('RMSE')
ttl = ax.title
ttl.set_position([.5, 1.08])
plt.title('RMSE Comparison of Regression Algorithms')
cnt = 0
for rect in bar:
    height = rect.get_height()
    ax.text(rect.get_x() + (rect.get_width()/2), 1.02*height,
            '%s' % str("{0:.2f}".format(performance[cnt])), ha='center', va='bottom')
    cnt += 1
plt.ylim([0, 3.5])
plt.savefig('graphGrubbs.png')  
plt.show()

aa1 = np.array(mae1).reshape(itr,4)
bb1 = aa1.mean(axis=0)
print(aa1.mean(axis=0))
fig, ax = plt.subplots()
objects = ('SVM', 'LiR', 'KNN', 'RFR')
y_pos = np.arange(len(objects))
performance = [bb1[0],bb1[1],bb1[2],bb1[3]]
bar = plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('MAE')
ttl = ax.title
ttl.set_position([.5, 1.08])
plt.title('MAE Comparison of Regression Algorithms')
cnt = 0
for rect in bar:
    height = rect.get_height()
    ax.text(rect.get_x() + (rect.get_width()/2), 1.02*height,
            '%s' % str("{0:.2f}".format(performance[cnt])), ha='center', va='bottom')
    cnt += 1
plt.ylim([0, 2])
plt.savefig('graphGrubbs.png')  
plt.show()

aa2 = np.array(mse).reshape(itr,4)
bb2 = aa2.mean(axis=0)
print(aa2.mean(axis=0))
fig, ax = plt.subplots()
objects = ('SVM', 'LiR', 'KNN', 'RFR')
y_pos = np.arange(len(objects))
performance = [bb2[0],bb2[1],bb2[2],bb2[3]]
bar = plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('MSE')
ttl = ax.title
ttl.set_position([.5, 1.08])
plt.title('MSE Comparison of Regression Algorithms')
cnt = 0
for rect in bar:
    height = rect.get_height()
    ax.text(rect.get_x() + (rect.get_width()/2), 1.02*height,
            '%s' % str("{0:.2f}".format(performance[cnt])), ha='center', va='bottom')
    cnt += 1
plt.ylim([0, 3.5])
plt.savefig('graphGrubbs.png')  
plt.show()
