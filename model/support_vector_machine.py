import numpy as np
import tensorflow as tf


class SVM(object):
    def __init__(learning_rate, epoch_count, batch_size, data_manager):
        self.__learning_rate = learning_rate
        self.__epoch = epoch_count
        self.__batch_size = batch_size
        self.__data_manager = data_manager

    def train(self):
        raise NotImplemented()

    def test(self):
        raise NotImplemented()

    def save(self, path):
        raise NotImplemented()

    def load(self, path):
        raise NotImplemented()
