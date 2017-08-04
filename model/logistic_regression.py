import tensorflow as tf

from base_model import BaseModel

class LogisticRegression(BaseModel):
    """
        Logistic regression class, inherits from BaseModel
    """

    def train(self):
        """
            Fit the logistic regression to the data
        """

        with tf.Session(graph=self._graph) as sess:
            x = tf.placeholder(tf.float32, [None, self._data_manager.get_feature_vec_len()])
            y = tf.placeholder(tf.float32, [None, self._data_manager.get_ground_truth_len()])

            W = tf.Variable(
                tf.zeros(
                    [
                        self._data_manager.get_feature_vec_len(),
                        self._data_manager.get_ground_truth_len()
                    ]
                )
            )
            b = tf.Variable(
                tf.zeros(
                    [
                        self._data_manager.get_ground_truth_len()
                    ]
                )
            )

            pred = tf.nn.softmax(tf.matmul(x, W) + b, name='predictions') # Softmax

            cost = tf.reduce_mean(
                -tf.reduce_sum(
                    y*tf.log(pred),
                    reduction_indices=1
                )
            )

            optimizer = tf.train.GradientDescentOptimizer(self._learning_rate).minimize(cost)

            init = tf.global_variables_initializer()

            sess.run(init)

            for e in range(self._epoch):
                self._data_manager.reset_current_batch_point()
                avg_cost = 0.
                total_batch = int(
                    self._data_manager.get_train_data_count() /
                    self._data_manager.get_batch_size()
                )

                print(self._data_manager.get_train_data_count())
                print(self._data_manager.get_batch_size())
                print(self._data_manager.get_feature_vec_len())
                print(self._data_manager.get_ground_truth_len())

                for i in range(total_batch):
                    print(i)
                    batch_data, batch_ground_truth = zip(*self._data_manager.get_next_train_batch())
                    _, c = sess.run(
                        [optimizer, cost],
                        feed_dict={x: batch_data, y: batch_ground_truth}
                    )
                    avg_cost += c / total_batch

                print("[+] Epoch: {}, cost: {}".format(e, format(avg_cost)))
