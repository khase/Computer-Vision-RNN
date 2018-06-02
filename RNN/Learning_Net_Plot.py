import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Flatten
from keras.utils import np_utils
from keras.utils import plot_model
import json
import os.path
import random


def loadBatch(data):

    random.shuffle(data)
    batchsize = 0
    input = []
    output = []
    for batch in data:
        index = 0
        if (batchsize == 0):
            batchsize = len(batch)
        else:
            if (batchsize != len(batch)):
                print("Error: Batchsize falsch!")
                continue
        for frame in batch:
            if index < batchsize-1:
                input.append(frame["Balls"][0]["Position"]["X"]/1920)
                input.append(frame["Balls"][0]["Position"]["Y"]/1080)
                input.append(frame["Balls"][0]["BoundingBox"]["Width"]/1920)
                input.append(frame["Balls"][0]["BoundingBox"]["Height"]/1080)
            else:
                output.append(frame["Balls"][0]["Position"]["X"]/1920)
                output.append(frame["Balls"][0]["Position"]["Y"]/1080)
                output.append(frame["Balls"][0]["BoundingBox"]["Width"]/1920)
                output.append(frame["Balls"][0]["BoundingBox"]["Height"]/1080)

            index += 1

    input = np.asarray(input)
    output = np.asarray(output)
    input = input.reshape((-1, batchsize-1, 4))  # The first index changing slowest, subseries as rows
    output = output.reshape((-1, 4))
    #print("input:")
    #print(input)
    #print("output:")
    #print(output)
    return (input, output)

with open("AugmentedBatches.json") as f:
    data = json.load(f)

#np.set_printoptions(threshold=np.inf)
model = Sequential()
#Since we know the shape of our Data we can input the timestep and feature data
#The number of timestep sequence are dealt with in the fit function
model.add(LSTM(512, return_sequences=True, input_shape=(4, 4)))
model.add(Dropout(0.2))
model.add(LSTM(512, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(512))
model.add(Dropout(0.2))
#number of features on the output
model.add(Dense(4, activation='softmax'))
print("Compile")
model.compile(loss='mean_squared_error', optimizer='adam')
plot_model(model, to_file='model.png')pip
