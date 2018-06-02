import json
import copy
from pprint import pprint
import sys
import numpy as np
import math

#function to bring f(x) = ax² + bx + c to f(x) = a(x-w) + s standard to vertex
def toVertexForm(a,b,c):
    w = -b/2*a
    s = c - (math.pow(b,2)/(4*a))
    return a,w,s

def calculate(parameter, x, scale):
    y = (scale * parameter[0]) * math.pow((x - parameter[1]),2) + parameter[2] 
    return y


#with open("Training-26.json") as f:
with open("Batches.json") as f:
    batches = json.load(f)
    print(str(len(batches)) + " batches loaded")
    #counter = 1
    augmentedBatches = []
    for batch in batches:
        #if(counter % 933 != 0):
        #    counter += 1
        #    continue
        newBatches = []
        for offset in range(-300, 301, 5):
            batchCopy = copy.deepcopy(batch)
            isBatchValid = True
            for frame in batchCopy:
                for ball in frame["Balls"]:
                    ball["Position"]["X"] += offset
                    # check if new position is actually inside the frame
                    if ball["Position"]["X"] < 0 or ball["Position"]["X"] > 1920:
                        isBatchValid = False
                    if not isBatchValid:
                        break
                if not isBatchValid:
                    break
            if isBatchValid:
                newBatches.append(batchCopy)
        #print some statistics    
        print(str(len(newBatches)) + " valid batches augmented")
        augmentedBatches.extend(newBatches)
    # print some statistics    
    print(str(len(augmentedBatches)) + " total batches augmented")

    # print Batches to disk
    #print("Writing Batches to: " + "./AugmentedBatches.json")
    #with open('AugmentedBatches.json', 'w') as outfile:
    #    json.dump(augmentedBatches, outfile, sort_keys=True, indent=2)
    
    # loop to stretch the square function
    #counter = 0
    for batch in batches:
        # Just to speed it up on my slug ^<^ 
        #if(counter % 1000 != 0):
        #    counter += 1
        #    continue
        newBatches = []
        #check if enough Points for an square function
        functionFound = False    
        if len(batch) >= 3:
            x = []
            y = []
            # need three points for the squarefunction
            for frame in batch:
                for ball in frame["Balls"]:
                    x = np.append(x,[ ball["Position"]["X"] ])
                    y = np.append(y,[ ball["Position"]["Y"] ])
                    # break cause i just wanna add the first ball of each frame
                    break;
                    # returns three values [a,b,c] corresponding to ax^2 + bx + c
            try:
                squareFunction = np.polyfit(x,y,2)
            except(np.RankWarning):
                print("No valid function found")
                functionFound= False
            else:
                functionFound = True
            if not functionFound:
                break

            vertexForm = toVertexForm(squareFunction[0], squareFunction[1], squareFunction[2] )
            for offset in np.arange(0, 1, 0.01):  
                batchCopy = copy.deepcopy(batch)
                isBatchValid = True 
                # use the square function to calculate the y-coordinate
                for frame in batchCopy:
                    for ball in frame["Balls"]:
                        # Stauchung
                        ball["Position"]["Y"] = calculate(vertexForm, ball["Position"]["X"], offset)
                        #print("Y = " + str(ball["Position"]["Y"]))
                        if ball["Position"]["Y"] < 0 or ball["Position"]["Y"] > 1080:
                            isBatchValid = False
                        if not isBatchValid:
                            break
                    if not isBatchValid:
                        break
                if isBatchValid:
                    newBatches.append(batchCopy)

                # translate the new curve in y direction
                for offset in range(-300, 301, 5):
                    secondBatchCopy = copy.deepcopy(batchCopy)
                    isBatchValid = True
                    for frame in secondBatchCopy:
                        for ball in frame["Balls"]:
                            ball["Position"]["Y"] += offset
                            #print("Y = " + str(ball["Position"]["Y"]))
                            if ball["Position"]["Y"] < 0 or ball["Position"]["Y"] > 1080:
                                isBatchValid = False
                            if not isBatchValid:
                                break
                        if not isBatchValid:
                            break
                    if isBatchValid:
                        newBatches.append(secondBatchCopy)
        #print some statistics    
        print(str(len(newBatches)) + " valid batches augmented")
        counter += 1
        print("Batch " + str(counter) + "/" + str(len(batches)) + "(" + str((counter*1.0)/len(batches)) + "%)")
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