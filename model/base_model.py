import numpy as np
import tensorflow as tf

class BaseModel(object):
    def __init__(self, learning_rate, epoch_count, data_manager, load_path=None):
        self._learning_rate = learning_rate
        self._epoch = epoch_count
        self._graph = tf.Graph()
        self._data_manager = data_manager
        self._session = tf.Session(graph=self._graph)

    def test(self):
        with self._graph.as_default():
            sess = self._session
            sess.run(tf.global_variables_initializer())
            good = np.zeros(self._data_manager.get_ground_truth_len())
            error = np.zeros(self._data_manager.get_ground_truth_len())
            total = np.zeros(self._data_manager.get_ground_truth_len())
            example_vecs, ground_truths = zip(*self._data_manager.get_test_data())
            pred = sess.graph.get_tensor_by_name('predictions:0')
            predictions = sess.run(pred, {'x:0': example_vecs})
            for i, pred in enumerate(predictions):
                pos = np.argmax(ground_truths[i])
                if np.argmax(pred[0]) == pos:
                    good[pos] += 1
                else:
                    error[pos] += 1

            print(
                'RESULTS:\n\tNORMAL: {}/{} => {}%\n\tDOS: {}/{} => {}%\n\tPROBE: {}/{} => {}%\n\tU2R: {}/{} => {}%\n\tR2L: {}/{} => {}%'.format(
                    good[0],
                    good[0] + error[0],
                    good[0] / float(good[0] + error[0]) * 100,
                    good[1],
                    good[1] + error[1],
                    good[1] / float(good[1] + error[1]) * 100
                    good[2],
                    good[2] + error[2],
                    good[2] / float(good[2] + error[2]) * 100
                    good[3],
                    good[3] + error[3],
                    good[3] / float(good[3] + error[3]) * 100
                    good[4],
                    good[4] + error[4],
                    good[4] / float(good[4] + error[4]) * 100
                )
            )

    def save(self, path):
        with open(path, 'wb') as f:
            f.write(
                tf.graph_util.convert_variables_to_constants(
                    self._session,
                    self._graph.as_graph_def(),
                    ['predictions']
                ).SerializeToString()
            )

    def load(self, path):
        with open(path, 'rb') as f:
            self._graph = tf.GraphDef()
            self._graph.ParseFromString(f.read())
            _ = tf.import_graph_def(self._graph, name='')
