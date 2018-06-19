from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
import json
import numpy as np
import random
import glob
import re
import sys


def sort_human(l,n):

  convert = lambda text: int(text) if text.isdigit() else text
  alphanum = lambda key: [ convert(c) for c in re.findall(r'\d+', key.split('\\')[n]) ]
  l.sort( key=alphanum )
  return l

def loadBatch(data):

    batchsize = 0
    lastFrame = 0
    firstFrame = 255
    input = []
    output = []
    for batch in data:
        index = 0
        if (batchsize == 0):
            batchsize = 5
        else:
            if (batchsize != len(batch)):
                print("Error: Batchsize falsch!")
                continue
        for frame in batch:
            if (index == 0):
                index += 1
                continue
            actFrameNr = int(frame["FrameNumber"])
            if (actFrameNr < firstFrame):
                firstFrame = actFrameNr
            if (actFrameNr > lastFrame):
                lastFrame = actFrameNr
            input.append(frame["Balls"][0]["Position"]["X"])
            input.append(frame["Balls"][0]["Position"]["Y"])
            output.append(actFrameNr)

            index += 1

    batchsize = batchsize - 1
    input = np.asarray(input)
    if (input.size == 0):
        return 0,0
    output = np.asarray(output)
    input = input.reshape((-1, batchsize, 2))  # The first index changing slowest, subseries as rows
    output = output.reshape((-1, batchsize, 1))  # The first index changing slowest, subseries as rows
    data = (input, output)
    frames = (firstFrame, lastFrame)
    #print(input)
    #print(output)
    return (data, frames)

model = Sequential()
#Since we know the shape of our Data we can input the timestep and feature data
#The number of timestep sequence are dealt with in the fit function
model.add(LSTM(20, return_sequences=True, input_shape=(4, 2)))
model.add(Dropout(0.5))
model.add(LSTM(20, return_sequences=True))
model.add(Dropout(0.5))
model.add(LSTM(20))
model.add(Dropout(0.5))
#number of features on the output
#model.add(LSTM(50, input_shape=(9, 4)))
#model.add(Dropout(0.2))
model.add(Dense(2, activation='linear'))
print("Compile")
model.compile(loss='mean_absolute_error', optimizer='adam')
print(model.summary())

file = "Own20_20_20_batch5.hdf5"
model.load_weights(file)



files = glob.glob("predictionBatches/Batches-*")
files = sort_human(files,1)
#print(files)
for filename in files:
    sys.stdout.write('\n')
    sys.stdout.flush()
    print(filename)
    with open(filename) as f:
        data = json.load(f)

    data, frames = loadBatch(data)
    if (data == 0):
        continue
    X, y = data
    firstFrame, lastFrame = frames
    predictedBatches = []
    predictedFramesNumbers = []
    #print("lastFrame: " + str(lastFrame))

    i = 0
    for batches in X:
        sys.stdout.write('.')
        sys.stdout.flush()
        #print(batches)
        randomStart = np.asarray(batches)
        predictions = []
        predictionsNumbers = []
        predictions.append(randomStart)
        predictionsNumbers.append(np.asarray(y[i]))
        for j in range(firstFrame+i,50):
            #print(j)
            x = np.reshape(randomStart, (1, len(randomStart), 2))
            #x=randomStart
            pred = model.predict(x)
            randomStart = np.vstack((randomStart, pred[0].astype(int)))
            randomStart = randomStart[1: len(randomStart)]
            #predictions.append(pred[0].astype(int))
            #predictions = np.vstack((predictions, pred.astype(int)))
            predictions = np.append(predictions, pred[0].astype(int))
            predictionsNumbers.append(firstFrame+i)
            #print(predictions)
        predictions = np.reshape(predictions, (1, int(len(predictions)/2), 2))
        predictionsNumbers = np.reshape(predictionsNumbers, (1, int(len(predictionsNumbers)), 1))
        predictedBatches.append(predictions)
        predictedFramesNumbers.append(predictionsNumbers)
        #print("Batches:")
        #print(predictedBatches)
        #print("i: " + str(i))

    #print("Complete Predicted:")
    #print(predictedBatches)
    testArray = [int(s) for s in re.findall(r'\d+', filename)]
    file = open("../Anotations/Prediction-" +str(testArray[0]) + ".json","w")
    file.write('[\n')
    j = 1
    for batch in predictedBatches:
        i = j
        file.write('[\n')
        for frame in batch[0]:
            if i > j:
                file.write(",\n")
            file.write("\t{")
            file.write('\n\t\t"FrameNumber": ' + str(i) +',\n')
            file.write('\t\t"Balls":\n')
            file.write('\t\t[\n')


            file.write('\n\t\t\t{\n')
            x = frame[0]
            y = frame[1]
            height = 40
            width = 40

            file.write('\t\t\t\t"Position": {"X": ' + str(x) + ', "Y": ' + str(y) +"},\n")
            file.write('\t\t\t\t"BoundingBox": {"Width": ' + str(width) + ', "Height": ' + str(height) +"}\n")

            i = i + 1
            file.write('\t\t\t}')

            file.write('\n\t\t]\n')
            file.write('\t}')


        file.write('],')
        j = j + 1
    file.write('[]]')
    file.close()
