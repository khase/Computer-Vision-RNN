import sys
import glob
import json
from pprint import pprint
import tensorflow as tf

def loadAnnotation(file):
    with open(file) as f:
        data = json.load(f)

    input = []
    output = []
    index = 0
    for frame in data:
        if index > 0:
            output.append(frame["balls"])
            input.append(lastframe["balls"])

        lastframe = frame;
        index += 1

    #print("input:")
    #pprint(input)
    #print("output:")
    #pprint(output)
    return (input, output)


for file in glob.glob("../Anotations/video5_images.txt"):
    loadAnnotation(file)

sys.exit

num_units = 200
num_layers = 3
dropout = tf.placeholder(tf.float32)

cells = []
for _ in range(num_layers):
  cell = tf.contrib.rnn.LSTMCell(num_units)  # Or GRUCell(num_units)
  cell = tf.contrib.rnn.DropoutWrapper(
      cell, output_keep_prob=1.0 - dropout)
  cells.append(cell)
cell = tf.contrib.rnn.MultiRNNCell(cells)

# Batch size x time steps x features.
data = tf.placeholder(tf.float32, [None, None, 28])
output, state = tf.nn.dynamic_rnn(cell, data, dtype=tf.float32)