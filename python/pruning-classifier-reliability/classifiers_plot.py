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

data = pd.read_csv('F18_pass_accuracy_grubb.csv')
ogdf = pd.read_csv('F18_stats_og.csv')
print(data.shape)

columns_target = ['Man of the Match'] 
#columns_train = ['Team', 'Opponent', 'Goal Scored', 'Ball Possession %', 'Attempts', 'On-Target','Off-Target','Blocked', 'Corners', 'Offsides', 'Free Kicks', 'Saves', 'Pass Accuracy %','Passes','Distance Covered (Kms)','Fouls Committed', 'Yellow Card', 'Yellow & Red', 'Red', '1st Goal', 'Round','PSO', 'Goals in PSO', 'Own goals', 'Own goal Time']
columns_train = ['Team', 'Opponent', 'Goal Scored', 'Ball Possession %', 'Attempts', 'On-Target','Off-Target', 'Corners', 'Pass Accuracy %','Passes']

data = data.dropna()

X = data[columns_train] 
Y = data[columns_target]
OX = ogdf[columns_train] 
OY = ogdf[columns_target]

from sklearn.model_selection import KFold

kf = KFold(n_splits=10)
kf.get_n_splits(X)
KFold(n_splits=10, random_state= 0, shuffle=False)
print("No of Splits: ", kf.get_n_splits(X))
itr = 1

for train_index, test_index in kf.split(X):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X.iloc[train_index], X.iloc[test_index] 
    Y_train, Y_test = Y.iloc[train_index], Y.iloc[test_index]

for train_index, test_index in kf.split(X):
    print("TRAIN:", train_index, "TEST:", test_index)
    OX_train, OX_test = OX.iloc[train_index], OX.iloc[test_index] 
    OY_train, OY_test = OY.iloc[train_index], OY.iloc[test_index]
    
#for i in range(itr):
for train_index, test_index in kf.split(X):
    a = list()
    linear_svc = LinearSVC()
    linear_svc.fit(X_train, np.ravel(Y_train)) 
    a.append(linear_svc.score(OX_test, OY_test))
    mlp = MLPClassifier(solver='adam', 
                        alpha=1e-2, 
                        hidden_layer_sizes=(21, 2), 
                        random_state=1)
    mlp.fit(X_train, np.ravel(Y_train)) 
    a.append(mlp.score(OX_test, OY_test))

    clf = LogisticRegression()
    clf.fit(X_train, np.ravel(Y_train)) 
    a.append(clf.score(OX_test, OY_test))

    knn=neighbors.KNeighborsClassifier()
    knn.fit(X_train, np.ravel(Y_train)) 
    a.append(knn.score(OX_test, OY_test))

    rfc = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
    rfc.fit(X_train, np.ravel(Y_train)) 
    a.append(rfc.score(OX_test, OY_test))

    decision_tree = DecisionTreeClassifier()
    decision_tree.fit(X_train, np.ravel(Y_train)) 
    a.append(decision_tree.score(OX_test, OY_test))

    bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1),
                             algorithm="SAMME",
                             n_estimators=200)
    bdt.fit(X_train, np.ravel(Y_train)) 
    a.append(bdt.score(OX_test, OY_test))

    bagging = BaggingClassifier(
        neighbors.KNeighborsClassifier(
            n_neighbors=8,
            weights='distance'
            ),
        oob_score=True,
        max_samples=0.5,
        max_features=1.0
        )
    bagging.fit(X_train, np.ravel(Y_train)) 
    a.append(bagging.score(OX_test, OY_test))

    gbm = xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05).fit(X_train, Y_train)
    gbm.fit(X_train, np.ravel(Y_train)) 
    a.append(gbm.score(OX_test, OY_test))

    print(a);
    
aa = np.array(a).reshape(itr,9)
bb = aa.mean(axis=0)
print(aa.mean(axis=0))
fig, ax = plt.subplots()
objects = ('SVC', 'MLP', 'LGR', 'KNN', 'RF', 'DT', 'AB','BC','GBM')
y_pos = np.arange(len(objects))
performance = [bb[0],bb[1],bb[2],bb[3],bb[4],bb[5],bb[6],bb[7],bb[8]]
bar = plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Accuracy')
ttl = ax.title
ttl.set_position([.5, 1.08])
plt.title('Machine Learning Algorithms (Grubb Test Pruning - Passes)')
cnt = 0
for rect in bar:
    height = rect.get_height()
    ax.text(rect.get_x() + (rect.get_width()/2), 1.02*height,
            '%s' % str("{0:.2f}".format(100*performance[cnt])) + "%", ha='center', va='bottom')
    cnt += 1
plt.ylim([0, 1.10])
plt.savefig('graphGrubbs.png')  
plt.show()

from sklearn.externals.six import StringIO  
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pydotplus
dot_data = StringIO()
export_graphviz(decision_tree, out_file=dot_data,
                feature_names=columns_train,
                filled=True, rounded=True,
                special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_pdf("iris.pdf")
