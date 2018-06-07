import json
import copy
from pprint import pprint
import sys
import numpy as np
import math
import matplotlib.pyplot as plt

# standarf -> vertex form:  f(x) = ax² + bx + c -> f(x) = a(x-w)² + s.
def toVertexForm(a,b,c):
    w = -b/(2*a)
    s = c - (math.pow(b,2)/(4*a))
    return a,w,s

def calculate(parameter, x, scale):
    y = (scale * parameter[0]) * math.pow((x - parameter[1]),2) + parameter[2]
    return y

def plotFunction(function, x=0, y=0, offset=1, vertex=True):
    plt.plot(x,y, 'bo')
    x1 = np.linspace(-999,1000,2000)
    if vertex:
        y1 = offset*(function[0]) * (x1 - function[1])*(x1 - function[1]) + function[2]
    else:
        y1 = function[0]*(x1*x1) + function[1]*x1 + function[2]
    #print(y1)
    plt.plot(x1,y1)
    plt.show()


#with open("Training-26.json") as f:
with open("Batches.json") as f:
    batches = json.load(f)
    print(str(len(batches)) + " batches loaded")
    #counter = 1
    augmentedBatches = []

    # print Batches to disk
    #print("Writing Batches to: " + "./AugmentedBatches.json")
    #with open('AugmentedBatches.json', 'w') as outfile:
    #    json.dump(augmentedBatches, outfile, sort_keys=True, indent=2)

    # loop to stretch the square function
    counter = 0
    for batch in batches:
        # Just to speed it up on my slug ^<^
        #if(counter % 300 != 0):
        #if(counter != 29):
        #    counter += 1
        #    continue
        newBatches = []
        #check if enough Points for an square function
        functionFound = False
        if len(batch) >= 3:
            xCoordinates = []
            yCoordinates = []
            # need three points for the squarefunction
            skippedFirstframe = False
            ballPos_X = 0
            ballPos_Y = 0
            for frame in batch:
                # skip the first Frame cause the ballposition there is always (0,0)
                #if not skippedFirstframe:
                #    skippedFirstframe = True
                #    continue
                for ball in frame["Balls"]:
                    ballPos_X += ball["Position"]["X"]
                    ballPos_Y += -ball["Position"]["Y"]
                    xCoordinates = np.append(xCoordinates,ballPos_X)
                    yCoordinates = np.append(yCoordinates,ballPos_Y)
                    # break cause i just wanna add the first ball of each frame
                    break
            try:
                # returns an array with three values [a,b,c] corresponding to ax^2 + bx + c
                squareFunction = np.polyfit(xCoordinates,yCoordinates,2)
            except(np.RankWarning):
                print("No valid function found")
                functionFound= False
            else:
                functionFound = True
            if not functionFound:
                break

            #plotFunction(squareFunction,xCoordinates,yCoordinates,1,False)

            vertexForm = toVertexForm(squareFunction[0], squareFunction[1], squareFunction[2])
            #plotFunction(vertexForm,xCoordinates,yCoordinates)
            #print(vertexForm)
            for offset in np.arange(0, 1, 0.01):
                if (offset == 0):
                    continue
                batchCopy = copy.deepcopy(batch)
                skippedFirstframe = False
                ballPos_X = 0
                ballPos_Y = 0
                firstBallPosition = 0
                oldBallPos_Y = 0
                oldBallPos_Y = 0
                frameNumber = 0
                newYCoordinates = []
                # use the square function to calculate the y-coordinate
                for frame in batchCopy:
                    for ball in frame["Balls"]:
                        if not skippedFirstframe:
                            firstBallPosition = -int(calculate(vertexForm, xCoordinates[frameNumber], offset))
                            relativePos_Y = 0
                            ball["Position"]["Y"] = relativePos_Y
                            oldBallPos_Y = firstBallPosition
                            skippedFirstframe = True
                            continue
                        # Stauchung
                        #print("x: " + str(xCoordinates[frameNumber]))
                        ballPos_Y = -int(calculate(vertexForm, xCoordinates[frameNumber], offset))
                        #newYCoordinates = np.append(newYCoordinates,ballPos_Y)
                        relativePos_Y = ballPos_Y - oldBallPos_Y
                        ball["Position"]["Y"] = relativePos_Y
                        oldBallPos_Y = ballPos_Y
                        break
                    frameNumber += 1
                #plotFunction(vertexForm, xCoordinates, newYCoordinates, offset)
                newBatches.append(batchCopy)
        #print some statistics
        print(str(len(newBatches)) + " valid batches augmented")
        counter += 1
        print("Batch " + str(counter) + "/" + str(len(batches)) + "(" + str((counter*100)/len(batches)) + "%)")
        augmentedBatches.extend(newBatches)
    # print some statistics
    print(str(len(augmentedBatches)) + " total batches augmented")

    # print Batches to disk
    print("Writing Batches to: " + "./AugmentedBatches.json")
    with open('AugmentedBatches.json', 'w') as outfile:
        json.dump(augmentedBatches, outfile, sort_keys=True, indent=2)

"""
#Check if there are some invalid Frames
counter = 0
with open("AugmentedBatches.json") as f:
    batches = json.load(f)
    print(str(len(batches)) + " batches loaded")
    for batch in batches:
            for frame in batch:
                for ball in frame["Balls"]:
                    if ball["Position"]["X"] < 0 or ball["Position"]["X"] > 1920:
                        print("Fehlerhaften Wert X gefunden")
                    if ball["Position"]["Y"] < 0 or ball["Position"]["Y"] > 1080:
                        print("Fehlerhaften Wert Y gefunden")
"""
