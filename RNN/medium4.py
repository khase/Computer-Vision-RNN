from __future__ import print_function, division
import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn
import matplotlib.pyplot as plt
import glob
import json

import sys

num_epochs = 50
total_series_length = 107
truncated_backprop_length = 5
state_size = 4
num_classes = 2
batch_size = 4
num_batches = total_series_length//batch_size//truncated_backprop_length

def loadAnnotation(file):
    with open(file) as f:
        data = json.load(f)

    input = []
    output = []
    index = 0
    for frame in data:
        if index > 0:
            if (len(frame["balls"]) > 0):
                output.append(frame["balls"][0]["position"]["x"])
                output.append(frame["balls"][0]["position"]["y"])
                output.append(frame["balls"][0]["boundingBox"]["width"])
                output.append(frame["balls"][0]["boundingBox"]["height"])
            else:
                output.append(0)
                output.append(0)
                output.append(0)
                output.append(0)

            if (len(lastframe["balls"]) > 0):
                input.append(lastframe["balls"][0]["position"]["x"])
                input.append(lastframe["balls"][0]["position"]["y"])
                input.append(lastframe["balls"][0]["boundingBox"]["width"])
                input.append(lastframe["balls"][0]["boundingBox"]["height"])
            else:
                input.append(0)
                input.append(0)
                input.append(0)
                input.append(0)


        lastframe = frame;
        index += 1

    input = np.asarray(input)
    output = np.asarray(output)
    input = input.reshape((-1, 4))  # The first index changing slowest, subseries as rows
    output = output.reshape((-1, 4))
    #print("input:")
    #pprint(input)
    #print("output:")
    #pprint(output)
    return (input, output)


def generateData(jsonFiles):
    x=[]
    y=[]
    for file in jsonFiles:
        a,b = loadAnnotation(file)
        x.append(a)
        y.append(b)


    #x = x.reshape((batch_size, -1))  # The first index changing slowest, subseries as rows
    #y = y.reshape((batch_size, -1))

    return (a, b)

def generateData2():
    x = np.array(np.random.choice(2, total_series_length, p=[0.5, 0.5]))
    y = np.roll(x, echo_step)
    y[0:echo_step] = 0

    x = x.reshape((batch_size, -1))  # The first index changing slowest, subseries as rows
    y = y.reshape((batch_size, -1))

    return (x, y)

batchX_placeholder = tf.placeholder(tf.float32, [truncated_backprop_length, state_size])
batchY_placeholder = tf.placeholder(tf.int32, [truncated_backprop_length, state_size])

cell_state = tf.placeholder(tf.float32, [batch_size, state_size])
hidden_state = tf.placeholder(tf.float32, [batch_size, state_size])
init_state = tf.nn.rnn_cell.LSTMStateTuple(cell_state, hidden_state)

W2 = tf.Variable(np.random.rand(state_size, num_classes),dtype=tf.float32)
b2 = tf.Variable(np.zeros((1,num_classes)), dtype=tf.float32)

# Unpack columns
inputs_series = tf.split(batchX_placeholder, truncated_backprop_length, 1)
labels_series = tf.unstack(batchY_placeholder, axis=1)

# Forward passes / OLD
#cell = tf.nn.rnn_cell.BasicLSTMCell(state_size, state_is_tuple=True)
#states_series, current_state = tf.nn.rnn(cell, inputs_series, init_state)

# Forward passes
cell = rnn.BasicLSTMCell(state_size)
states_series, current_state = rnn.static_rnn(cell, inputs_series, dtype=tf.float32)


logits_series = [tf.matmul(state, W2) + b2 for state in states_series] #Broadcasted addition
predictions_series = [tf.nn.softmax(logits) for logits in logits_series]

losses = [tf.nn.sparse_softmax_cross_entropy_with_logits(logits = logits, labels = labels) for logits, labels in zip(logits_series,labels_series)]
total_loss = tf.reduce_mean(losses)

train_step = tf.train.AdagradOptimizer(0.3).minimize(total_loss)

def plot(loss_list, predictions_series, batchX, batchY):
    plt.subplot(2, 3, 1)
    plt.cla()
    plt.plot(loss_list)

    for batch_series_idx in range(5):
        one_hot_output_series = np.array(predictions_series)[:, batch_series_idx, :]
        single_output_series = np.array([(1 if out[0] < 0.5 else 0) for out in one_hot_output_series])

        plt.subplot(2, 3, batch_series_idx + 2)
        plt.cla()
        plt.axis([0, truncated_backprop_length, 0, 2])
        left_offset = range(truncated_backprop_length)
        plt.bar(left_offset, batchX[batch_series_idx, :], width=1, color="blue")
        plt.bar(left_offset, batchY[batch_series_idx, :] * 0.5, width=1, color="red")
        plt.bar(left_offset, single_output_series * 0.3, width=1, color="green")

    plt.draw()
    plt.pause(0.0001)


jsonFiles = glob.glob("../Anotations/*.json")
#np.random.shuffle(jsonFiles)
#x,y = generateData(jsonFiles)
#print("x: ")
#print(x)
#print("y: ")
#print(y)
with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())
    plt.ion()
    plt.figure()
    plt.show()
    loss_list = []

    for epoch_idx in range(num_epochs):
        np.random.shuffle(jsonFiles)
        x,y = generateData(jsonFiles)
        _current_cell_state = np.zeros((batch_size, state_size))
        _current_hidden_state = np.zeros((batch_size, state_size))

        print("New data, epoch", epoch_idx)

        for batch_idx in range(num_batches):
            start_idx = batch_idx * truncated_backprop_length
            end_idx = start_idx + truncated_backprop_length

            batchX = x[:,start_idx:end_idx]
            batchY = y[:,start_idx:end_idx]

            _total_loss, _train_step, _current_state, _predictions_series = sess.run(
                [total_loss, train_step, current_state, predictions_series],
                feed_dict={
                    batchX_placeholder: batchX,
                    batchY_placeholder: batchY,
                    cell_state: _current_cell_state,
                    hidden_state: _current_hidden_state

                })

            _current_cell_state, _current_hidden_state = _current_state

            loss_list.append(_total_loss)

            #if batch_idx%100 == 0:
            print("Step",batch_idx, "Batch loss", _total_loss)
            plot(loss_list, _predictions_series, batchX, batchY)

plt.ioff()
plt.show()
