import os
import errno
import argparse

import numpy as np
import tensorflow as tf

# Data loader/manager
from data_manager import DataManager

# Models
from logistic_regression import LogisticRegression
from support_vector_machine import SVM
from feed_forward_neural_network import FeedForwardNN
from lstm_network import LSTMNN

def parse_arguments():
    """
        Parse the command line arguments of the program.
    """
    
    parser = argparse.ArgumentParser(description='Train a model on data.')
    parser.add_argument(
        "data_dir",
        type=str,
        nargs="?",
        help="The data directory",
    )
    parser.add_argument(
        "output_dir",
        type=str,
        nargs="?",
        help="The output directory",
        default="out/",
    )
    parser.add_argument(
        "-c",
        "--epoch_count",
        type=int,
        nargs="?",        
        help="Number of training steps.",
        default=100
    )
    parser.add_argument(
        "-l",
        "--learning_rate",
        type=float,
        nargs="?",        
        help="The initial learning rate.",
        default=0.01
    )
    parser.add_argument(
        "-r",
        "--train_test_ratio",
        type=float,
        nargs="?",        
        help="The ratio between train and test examples in the data.",
        default=0.85
    )
    parser.add_argument(
        "-m",
        "--model",
        type=int,
        nargs="?",
        help="The model to use:\n \tLogReg (1)\n \tSVM (2)\n \tFeedForwardNN (3)\n \tLSTMNN (4)"
    )

    return parser.parse_args()

def main():
    """
        Description: Train the model, outputs the performance, saves the .pb
        Usage: python run.py [data_dir] [ratio] [out_dir] [epoch_count]
    """

    # Parse the arguments
    args = parse_arguments()

    # Create the directory if it does not exist.
    try:
        os.makedirs(args.output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    data_manager = DataManager(args.data_dir, args.train_test_ratio)

    model = None

    îf args.model == 1:
        model = LogisticRegression()
    elif args.model == 2:
        model = SVM()
    elif args.model == 3:
        model = FeedForwardNN()
    elif args.model == 4:
        model = LSTMNN()
    else:
        raise Exception("Unknown model")

if __name__=='__main__':
    main()
