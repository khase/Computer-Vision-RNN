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
    print("input:")
    print(input)
    print("output:")
    print(output)
    return (input, output)

with open("AugmentedBatches.json") as f:
    data = json.load(f)

#np.set_printoptions(threshold=np.inf)
model = Sequential()
#Since we know the shape of our Data we can input the timestep and feature data
#The number of timestep sequence are dealt with in the fit function
model.add(LSTM(2048, input_shape=(4, 4)))
model.add(Dropout(0.2))
#number of features on the output
model.add(Dense(4, activation='softmax'))
print("Compile")
model.compile(loss='categorical_crossentropy', optimizer='adam')
print(model.summary())
print("Fit")
for n in range(10):
    X,y = loadBatch(data)
    print (n)
    if (os.path.isfile("Own.hdf5")):
        model.load_weights("Own.hdf5")
    model.fit(X, y, epochs=10, batch_size=1000)
    model.save_weights("Own.hdf5")
print("Finished")

mult = [1920,1080,1920,1080]

for i in range(2):
    randomVal = np.random.randint(0, len(X)-1)
    randomStart = X[randomVal]
    x = np.reshape(randomStart, (1, len(randomStart), 4))
    pred = model.predict(x)
    print("Start:")
    randomStart = np.multiply(randomStart,mult)
    print(randomStart)
    print("pred:")
    pred = np.multiply(pred,mult)
    print(pred)
    print("Real")
    real = y[randomVal]
    real = np.multiply(real,mult)
    print(real)