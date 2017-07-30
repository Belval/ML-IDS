import numpy as np
import tensorflow as tf

class BaseModel(object):
    def __init__(learning_rate, epoch_count, batch_size, data_manager, load_path=None):
        self.__learning_rate = learning_rate
        self.__epoch = epoch_count
        self.__batch_size = batch_size
        self.__data_manager = data_manager
        self.__graph = tf.Graph()

        # If a path was given, load it
        if load_path != None:
            self.load(load_path)
    
    def test(self):
        with tf.Session(graph=self.__graph) as sess:                
            label_lines = labels.split('\n')
            sess.run(tf.global_variables_initializer())
            good = np.zeros(self.__data_manager.get_ground_truth_len())
            error = np.zeros(self.__data_manager.get_ground_truth_len())
            total = np.zeros(self.__data_manager.get_ground_truth_len())
            for example_vec, ground_truth in self.__data_manager.get_test_data():
                pred = sess.graph.get_tensor_by_name('predictions:0')
                predictions = sess.run(pred, {'x:0': example_vec})
                if predictions[0] == ground_truth:
                    good[ground_truth.index(1)] += 1
                else:
                    bad[ground_truth.index(1)] += 1
            
            print(
                'RESULTS:\n\tNORMAL: {}/{}\n\tDOS: {}/{}\n\tPROBE: {}/{}\n\tU2R: {}/{}\n\tR2L: {}/{}'.format(
                    good[0],
                    good[0] + bad[0],
                    good[1],
                    good[1] + bad[1],
                    good[2],
                    good[2] + bad[2],
                    good[3],
                    good[3] + bad[3],
                    good[4],
                    good[4] + bad[4],
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
            self.__graph = tf.GraphDef()
            self.__graph.ParseFromString(f.read())
            _ = tf.import_graph_def(self.__graph, name='')
