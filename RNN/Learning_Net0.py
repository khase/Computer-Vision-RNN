import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Flatten
from keras.utils import np_utils
from keras.utils import plot_model
from keras.callbacks import CSVLogger
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
            if (index == 0):
                index += 1
                continue
            if index < batchsize-1:
                input.append(frame["Balls"][0]["Position"]["X"])
                input.append(frame["Balls"][0]["Position"]["Y"])
                #input.append(frame["Balls"][0]["BoundingBox"]["Width"])
                #input.append(frame["Balls"][0]["BoundingBox"]["Height"])
            else:
                output.append(frame["Balls"][0]["Position"]["X"])
                output.append(frame["Balls"][0]["Position"]["Y"])
                #output.append(frame["Balls"][0]["BoundingBox"]["Width"])
                #output.append(frame["Balls"][0]["BoundingBox"]["Height"])

            index += 1

    batchsize = batchsize - 1
    input = np.asarray(input)
    output = np.asarray(output)
    input = input.reshape((-1, batchsize-1, 2))  # The first index changing slowest, subseries as rows
    output = output.reshape((-1, 2))
    #print("input:")
    #print(input)
    #print("output:")
    #print(output)
    return (input, output)

batchsize = 0
with open("AugmentedBatchesNew.json") as f:
    data = json.load(f)

#np.set_printoptions(threshold=np.inf)
model = Sequential()
#Since we know the shape of our Data we can input the timestep and feature data
#The number of timestep sequence are dealt with in the fit function
model.add(LSTM(20, return_sequences=True, input_shape=(4, 2)))
model.add(Dropout(0.4))
model.add(LSTM(20, return_sequences=True))
model.add(Dropout(0.4))
model.add(LSTM(20))
model.add(Dropout(0.4))
#number of features on the output
#model.add(LSTM(50, input_shape=(9, 4)))
#model.add(Dropout(0.2))
model.add(Dense(2, activation='linear'))
print("Compile")
model.compile(loss='mean_absolute_error', optimizer='adam')
print(model.summary())
runs = 1
#for n in range(5):
csv_logger = CSVLogger('log20_20_20_batch5.txt', append=True, separator=';')
file = "Own20_20_20_batch5.hdf5"
while True:
    print ("Run no. " + str(runs) + ". Shuffling Data....")
    runs = runs + 1
    X,y = loadBatch(data)
    if (os.path.isfile(file)):
        print("Loading Weights")
        model.load_weights(file)
    model.fit(X, y, epochs=20, batch_size=1000, callbacks=[csv_logger])
    print("Saving Weights")
    model.save_weights(file)
