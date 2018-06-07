from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
import json
import numpy as np
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
                input.append(frame["Balls"][0]["Position"]["X"])
                input.append(frame["Balls"][0]["Position"]["Y"])
                input.append(frame["Balls"][0]["BoundingBox"]["Width"])
                input.append(frame["Balls"][0]["BoundingBox"]["Height"])
            else:
                output.append(frame["Balls"][0]["Position"]["X"])
                output.append(frame["Balls"][0]["Position"]["Y"])
                output.append(frame["Balls"][0]["BoundingBox"]["Width"])
                output.append(frame["Balls"][0]["BoundingBox"]["Height"])

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

model = Sequential()
#Since we know the shape of our Data we can input the timestep and feature data
#The number of timestep sequence are dealt with in the fit function
model.add(LSTM(10, input_shape=(9, 4)))
model.add(Dropout(0.2))
model.add(Dense(4, activation='softmax'))
print("Compile")
model.compile(loss='mean_squared_error', optimizer='adam')
print(model.summary())

model.load_weights("Own40.hdf5")


X,y = loadBatch(data)
predictions = []
for i in range(0,10):
    #randomVal = np.random.randint(0, len(X)-1)
    randomStart = X[i]
    x = np.reshape(randomStart, (1, len(randomStart), 4))
    pred = model.predict(x)
    #print("Start:")
    #randomStart = np.multiply(randomStart,mult)
    #print(randomStart)
    real = y[i]
    print(x)
    print(pred.astype(int))
    print(real.astype(int))
    diff = real-pred
    print(str(i) + " " + str(diff.astype(int)))
    predictions.append(pred[0].astype(int))

#print("Predictions:")
#print(predictions)

predicted = []
for i in range(0,10):
    predicted.append(X[i][0].astype(int))
    predicted.append(X[i][1].astype(int))
    predicted.append(X[i][2].astype(int))
    predicted.append(X[i][3].astype(int))
    predicted.append(X[i][4].astype(int))
    predicted.append(X[i][5].astype(int))
    predicted.append(X[i][6].astype(int))
    predicted.append(X[i][7].astype(int))
    predicted.append(X[i][8].astype(int))
    predicted.append(predictions[i])

predicted = np.reshape(predicted, (len(predicted), 4))

print("Complete Predicted:")
print(predicted)
j = 0
file = open("PredictedBatches" + ".json","w")
file.write('[\n')
for frame in predicted:
    if j > 0:
        file.write(",\n")
    file.write("\t{")
    file.write('\n\t\t"FrameNumber": ' + str(j) +',\n')
    file.write('\t\t"Balls":\n')
    file.write('\t\t[\n')

    i = 0

    file.write('\n\t\t\t{\n')
    x = frame[0]
    y = frame[1]
    height = frame[2]
    width = frame[3]

    file.write('\t\t\t\t"Position": {"X": ' + str(x) + ', "Y": ' + str(y) +"},\n")
    file.write('\t\t\t\t"BoundingBox": {"Width": ' + str(width) + ', "Height": ' + str(height) +"}\n")

    i = i + 1
    file.write('\t\t\t}')

    j = j + 1
    file.write('\n\t\t]\n')
    file.write('\t}')

file.write(']')
file.close()
