import numpy as np
import tensorflow as tf


class LSTMNN(object):
    def __init__(learning_rate, epoch_count, batch_size, data_manager, load_path=None):
        BaseModel.__init__(learning_rate, epoch_count, batch_size, data_manager, load_path)
    
    def train(self):
        raise NotImplemented()

    def test(self):
        raise NotImplemented()

    def save(self, path):
        raise NotImplemented()

    def load(self, path):
        raise NotImplemented()
