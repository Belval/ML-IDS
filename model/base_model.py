import numpy as np
import tensorflow as tf

class BaseModel(object):
    def __init__(self, learning_rate, epoch_count, data_manager, load_path=None):
        self._learning_rate = learning_rate
        self._epoch = epoch_count
        self._graph = tf.Graph()
        self._data_manager = data_manager

    def test(self):
        with tf.Session(graph=self._graph) as sess:
            label_lines = labels.split('\n')
            sess.run(tf.global_variables_initializer())
            good = np.zeros(self._data_manager.get_ground_truth_len())
            error = np.zeros(self._data_manager.get_ground_truth_len())
            total = np.zeros(self._data_manager.get_ground_truth_len())
            for example_vec, ground_truth in self._data_manager.get_test_data():
                pred = sess.graph.get_tensor_by_name('predictions:0')
                predictions = sess.run(pred, {'x:0': example_vec})
                if predictions[0] == ground_truth:
                    good[ground_truth.index(1)] += 1
                else:
                    error[ground_truth.index(1)] += 1

            print(
                'RESULTS:\n\tNORMAL: {}/{}\n\tDOS: {}/{}\n\tPROBE: {}/{}\n\tU2R: {}/{}\n\tR2L: {}/{}'.format(
                    good[0],
                    good[0] + error[0],
                    good[1],
                    good[1] + error[1],
                    good[2],
                    good[2] + error[2],
                    good[3],
                    good[3] + error[3],
                    good[4],
                    good[4] + error[4],
                )
            )

    def save(self, path):
        with open(path, 'wb') as f:
            f.write(
                graph_util.convert_variables_to_constants(
                    sess,
                    tf.get_default_graph().as_graph_def(),
                    ['predictions']
                ).SerializeToString()
            )

    def load(self, path):
        with open(path, 'rb') as f:
            self._graph = tf.GraphDef()
            self._graph.ParseFromString(f.read())
            _ = tf.import_graph_def(self._graph, name='')
