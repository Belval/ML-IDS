import os
import gzip
import numpy as np

class DataManager(object):
    """
        DataManager class, load, parse, and acts as a data source
        for all the models in the project
    """

    def __init__(self, path, ratio, batch_size):
        """
            Constructor
        """

        self.path = path
        self.ratio = ratio
        self.__ground_truth_len = 5
        self.__current_batch_point = 0
        self.__batch_size = batch_size
        self.__PROTOCOLS = ["tcp", "udp", "icmp"]
        self.__SERVICES = ["rje", "ntp_u", "kshell", "bgp", "iso_tsap", "X11", "whois", "supdup", "discard", "ftp", "tim_i", "uucp", "smtp", "vmnet", "pm_dump", "netstat", "http", "efs", "domain", "echo", "systat", "IRC", "tftp_u", "telnet", "csnet_ns", "printer", "login", "netbios_dgm", "netbios_ns", "harvest", "hostnames", "aol", "pop_2", "ssh", "mtp", "name", "http_8001", "auth", "urh_i", "shell", "http_2784", "daytime", "ldap", "uucp_path", "time", "domain_u", "remote_job", "urp_i", "Z39_50", "http_443", "nnsp", "exec", "imap4", "red_i", "pop_3", "ctf", "sql_net", "ecr_i", "netbios_ssn", "courier", "private", "other", "link", "finger", "gopher", "eco_i", "ftp_data", "nntp", "sunrpc", "klogin"]
        self.__FLAGS = ["RSTOS0", "OTH", "SF", "S1", "RSTO", "REJ", "SH", "RSTR", "S3", "S0", "S2"]
        self.__OUTPUT_VALUES = ["normal", "dos", "probe", "u2r", "r2l"]
        self.__FEATURE_VEC_LEN = 38 + len(self.__PROTOCOLS) + len(self.__SERVICES) + len(self.__FLAGS)
        self.__TYPE_MAP = {
            "buffer_overflow": 3,
            "back": 1,
            "pod": 1,
            "portsweep": 2,
            "land": 1,
            "warezclient": 4,
            "smurf": 1,
            "spy": 4,
            "teardrop": 1,
            "perl": 3,
            "rootkit": 3,
            "nmap": 2,
            "imap": 4,
            "ftp_write": 4,
            "multihop": 4,
            "guess_passwd": 4,
            "satan": 2,
            "normal": 0,
            "ipsweep": 2,
            "neptune": 1,
            "loadmodule": 3,
            "phf": 4,
            "warezmaster": 4
        }

        self.__load_data()

    def __load_data(self):
        """
            Loads the gunzipped data into a numpy array
        """

        self.__data = []
        with gzip.open(os.path.join(self.path, 'kdd_data.gz'), 'r') as f:
            for i, l in enumerate(f.readlines()):
                example = l.split(b',')
                example_vec = np.zeros(self.__FEATURE_VEC_LEN)
                ground_truth = np.zeros(5)
                ground_truth[self.__TYPE_MAP[example[-1].decode("utf-8") .replace('\n', '').replace('.', '')]] = 1
                del example[-1]
                for i, v in enumerate(example):
                    if i == 0:
                        example_vec[i] = float(v)
                    elif i == 1:
                        example_vec[self.__PROTOCOLS.index(v.decode("utf-8"))] = 1
                    elif i == 2:
                        example_vec[self.__SERVICES.index(v.decode("utf-8")) + 2] = 1
                    elif i == 3:
                        example_vec[self.__FLAGS.index(v.decode("utf-8")) + 69 + 2] = 1
                    else:
                        example_vec[i + 10 + 69 + 2] = float(v)
                self.__data.append((example_vec, ground_truth))

        self.__example_count = np.shape(self.__data)[0]

        with open(os.path.join(self.path, 'kdd_labels.txt'), 'r') as f:
            self.__labels = f.readlines()

    def get_train_data(self):
        """
            Return the training data
        """

        return self.__data[0:self.get_train_data_count()]

    def get_next_train_batch(self):
        """
            Return the next batch of data for training
        """

        train_data = self.get_train_data()[
            self.__current_batch_point * self.__batch_size:
            (self.__current_batch_point + 1) * self.__batch_size
        ]
        self.__current_batch_point += 1
        return train_data

    def get_train_data_count(self):
        """
            Return the number of training examples
        """

        return int(self.__example_count * self.ratio)

    def get_test_data(self):
        """
            Return the test data
        """

        return self.__data[self.get_test_data_count():]

    def get_test_data_count(self):
        """
            Return the number of testing examples
        """

        return int(self.__example_count - self.get_train_data_count())

    def get_batch_size(self):
        """
            Return the batch size
        """

        return self.__batch_size

    def get_feature_vec_len(self):
        """
            Return the length of the feature vector
        """

        return len(self.__data[0][0])

    def get_ground_truth_len(self):
        """
            Return the length of the ground truth vector
            (The number of classes)
        """

        return self.__ground_truth_len

    def reset_current_batch_point(self):
        self.__current_batch_point = 0