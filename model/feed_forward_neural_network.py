import numpy as np
import tensorflow as tf


class FeedForwardNN(BaseModel):
    def __init__(learning_rate, epoch_count, batch_size, data_manager, load_path):
        BaseModel.__init__(learning_ratem epoch_count, batch_size, data_manager, load_path=None)

    def train(self):
        x = tf.placeholder(tf.float32, [None, self.__feature_count])
        y = tf.placeholder(tf.float32, [None, self.__output_size])

        W_1 = tf.Variable(tf.zeros([self.__feature_count, self.__output_size]))
        b_1 = tf.Variable(tf.zeros([self.__output_size]))

        hidden_1 = tf.nn.softmax(tf.matmul(x, W) + b) # Softmax

        W_2 = tf.Variable(tf.zeros([self.__feature_count, self.__output_size]))
        b_2 = tf.Variable(tf.zeros([self.__output_size]))

        hidden_2 = tf.nn.softmax(tf.matmul(x, W) + b) # Softmax

        W_3 = tf.Variable(tf.zeros([self.__feature_count, self.__output_size]))
        b_3 = tf.Variable(tf.zeros([self.__output_size]))

        pred = tf.nn.softmax(tf.matmul(x, W) + b) # Softmax

        cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred), reduction_indices=1))

        optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

        init = tf.global_variables_initializer()

        with tf.Session(graph=self.__graph) as sess:
            sess.run(init)

            for epoch in range(training_epochs):
                avg_cost = 0.
                total_batch = int(data_manager.get_train_data_count() / batch_size)
                for i in range(total_batch):
                    batch_data, batch_ground_truth = data_manager.get_next_train_batch()
                    _, c = sess.run([optimizer, cost], feed_dict={x: batch_data, y: batch_ground_truth})
                    avg_cost += c / total_batch

                print("[+] Epoch: {}, cost: {}".format(epoch, format(avg_cost)))
