import numpy as np
import tensorflow as tf


class SVM(BaseModel):
    def __init__(learning_rate, epoch_count, batch_size, data_manager, load_path=None):
        BaseModel.__init__(learning_rate, epoch_count, batch_size, data_manager, load_path)

    def train(self):
        x = tf.placeholder(tf.float32, [None, self.__feature_count])
        y = tf.placeholder(tf.float32, [None, self.__output_size])
