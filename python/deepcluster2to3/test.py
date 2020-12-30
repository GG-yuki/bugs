import os
import pickle
import clustering
class Logger():
    """ Class to update every epoch to keep trace of the results
    Methods:
        - log() log and save
    """

    def __init__(self, path):
        self.path = path
        self.data = []

    def log(self, train_point):
        self.data.append(train_point)
        with open(os.path.join(self.path), 'wb') as fp:
            pickle.dump(self.data, fp, -1)
        print('ok')

cluster_log = Logger(os.path.join('./image_list_log/','clusters'))

cluster_log.log([[1,3,5],[2,4,6]])
cluster_log.log([[1,2,3],[4,5,6]])
print(clustering.arrange_clustering(cluster_log.data[-1]))
