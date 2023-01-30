# https://www.tensorflow.org/tutorials/keras/overfit_and_underfit?hl=ko

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import regularizers

import tensorflow_docs as tfdocs
import tensorflow_docs.modeling
import tensorflow_docs.plots

from IPython import display
from matplotlib import pyplot as plt

import numpy as np

import pathlib
import shutil
import tempfile

logdir = pathlib.Path(tempfile.mkdtemp())/"tensorboard_logs"
print(logdir)
shutil.rmtree(logdir, ignore_errors=True)

gz = tf.keras.utils.get_file('HIGGS.csv.gz',
                             'http://mlphysics.ics.uci.edu/data/higgs/HIGGS.csv.gz',
                             cache_dir='/Users/youranwoo/workspace/tensorflow/tdc_practice/tutorial/basic',
                             cache_subdir='dataset')

FEATURES = 28
ds = tf.data.experimental.CsvDataset(gz,[float(),]*(FEATURES+1), compression_type="GZIP")

def pack_row(*row):
  label = row[0]
  features = tf.stack(row[1:],1)
  return features, label

packed_ds = ds.batch(10000).map(pack_row).unbatch()

for features,label in packed_ds.batch(1000).take(1):
  print(features[0])
  # plt.hist(features.numpy().flatten(), bins = 101)
  # plt.show()

N_VALIDATION = int(1e3)
N_TRAIN = int(1e4)
BUFFER_SIZE = int(1e4)
BATCH_SIZE = 500
STEPS_PER_EPOCH = N_TRAIN//BATCH_SIZE

validate_ds = packed_ds.take(N_VALIDATION).cache()
train_ds = packed_ds.skip(N_VALIDATION).take(N_TRAIN).cache()
print(train_ds)