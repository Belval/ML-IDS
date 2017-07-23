import os
import numpy as np

class DataManager(object):
    def __init__(self, path, ratio):
        self.path = path
        self.ratio = ratio
        self.__load_data()

    def __load_data(self):
        self.__data = np.loadtxt(os.path.join(self.path, 'kdd_data.gz'))
        self.__example_count = np.shape(self.__data)[0]
        with open(os.path.join(path, 'kdd_labels.txt'), 'r') as f:
            self.__labels = f.readlines()

    def get_train_data(self):
        train_data_count = self.__example_count * self.ratio
        return self.__data[0:train_data_count]

    def get_test_data(self):
        train_data_count = self.__example_count * self.ratio
        return self.__data[train_data_count:]

