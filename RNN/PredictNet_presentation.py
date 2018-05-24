from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
import json
import numpy as np
import random

def loadBatch(data):

    #random.shuffle(data)
    batchsize = 0
    input = []
    output = []
    outerIndex = 0

    for i in range(0,6):
        index = 0
        for frame in data:
            print(index)
            print(outerIndex)
            if index <= outerIndex:
                index += 1
                continue
            if index < outerIndex + 5:
                input.append(frame["Balls"][0]["Position"]["X"]/1920)
                input.append(frame["Balls"][0]["Position"]["Y"]/1080)
                input.append(frame["Balls"][0]["BoundingBox"]["Width"]/1920)
                input.append(frame["Balls"][0]["BoundingBox"]["Height"]/1080)
            else:
                output.append(frame["Balls"][0]["Position"]["X"]/1920)
                output.append(frame["Balls"][0]["Position"]["Y"]/1080)
                output.append(frame["Balls"][0]["BoundingBox"]["Width"]/1920)
                output.append(frame["Balls"][0]["BoundingBox"]["Height"]/1080)
                break
            index += 1
        outerIndex += 1

    input = np.asarray(input)
    output = np.asarray(output)
    input = input.reshape((-1, 4, 4))  # The first index changing slowest, subseries as rows
    output = output.reshape((-1, 4))
    print("input:")
    print(input)
    print("output:")
    print(output)
    return (input, output)

with open("Training-14.json") as f:
    data = json.load(f)

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

model.load_weights("Own512_3.hdf5")

mult = [1920,1080,1920,1080]

X,y = loadBatch(data)
predictions = []
for i in range(0,6):
    #randomVal = np.random.randint(0, len(X)-1)
    randomStart = X[i]
    x = np.reshape(randomStart, (1, len(randomStart), 4))
    pred = model.predict(x)
    #print("Start:")
    #randomStart = np.multiply(randomStart,mult)
    #print(randomStart)
    real = y[i]
    real = np.multiply(real,mult)
    pred = np.multiply(pred,mult)
    print(pred.astype(int))
    print(real.astype(int))
    diff = real-pred
    print(str(i) + " " + str(diff.astype(int)))
    predictions.append(pred[0].astype(int))

print("Predictions:")
print(predictions)

predicted = []
predicted.append(np.multiply(X[0][0],mult).astype(int))
predicted.append(np.multiply(X[1][0],mult).astype(int))
predicted.append(np.multiply(X[2][0],mult).astype(int))
predicted.append(np.multiply(X[3][0],mult).astype(int))
for i in range(0,6):
    predicted.append(predictions[i])

predicted = np.reshape(predicted, (len(predicted), 4))

print("Complete Predicted:")
print(predicted)
j = 0
file = open("Prediction-14" + ".json","w")
file.write('[\n')
for frame in predicted:
    if j > 0:
        file.write(",\n")
    file.write("\t{")
    file.write('\n\t\t"frameNumber": ' + str(j) +',\n')
    file.write('\t\t"balls":\n')
    file.write('\t\t[\n')

    i = 0

    file.write('\n\t\t\t{\n')
    x = frame[0]
    y = frame[1]
    height = frame[2]
    width = frame[3]

    file.write('\t\t\t\t"position": {"x": ' + str(x) + ', "y": ' + str(y) +"},\n")
    file.write('\t\t\t\t"boundingBox": {"width": ' + str(width) + ', "height": ' + str(height) +"}\n")

    i = i + 1
    file.write('\t\t\t}')

    j = j + 1
    file.write('\n\t\t]\n')
    file.write('\t}')

file.write(']')
file.close()
