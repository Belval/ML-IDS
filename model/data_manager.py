import os
import gzip
import numpy as np

class DataManager(object):
    def __init__(self, path, ratio):
        self.path = path
        self.ratio = ratio
        self.__load_data()

    def __load_data(self):
        self.__data = []
        with gzip.open(os.path.join(self.path, 'kdd_data.gz'), 'r') as f:
            for i, l in enumerate(f.read().split(b'.')):
                print(i)
                example = l.split(b',')
                example_as_list = []
                for v in example:
                    try:
                        example_as_list.append(float(v))
                    except:
                        example_as_list.append(v)
                self.__data.append(example_as_list)

        self.__example_count = np.shape(self.__data)[0]
        with open(os.path.join(self.path, 'kdd_labels.txt'), 'r') as f:
            self.__labels = f.readlines()

        print(self.__example_count)

    def get_train_data(self):
        train_data_count = self.__example_count * self.ratio
        return self.__data[0:train_data_count]

    def get_test_data(self):
        train_data_count = self.__example_count * self.ratio
        return self.__data[train_data_count:]

