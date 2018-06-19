import json
import copy
import glob
import re
from pprint import pprint

BatchSize = 5

jsonFiles = glob.glob("..\Anotations\Training*.json")
print("Files found: " + str(len(jsonFiles)))

# collect all frames from annotations
for file in jsonFiles:
    fileNumber = [int(s) for s in re.findall(r'\d+', file.split('\\')[2])][0]
    allFrames = []
    with open(file) as f:
        data = json.load(f)
        
        for frame in data:
            allFrames.append(frame)

    # print some statistics
    print("Total Framecount: " + str(len(allFrames)))
    # frames with annotated balls are "valid"
    validFrames = []
    invalidFrameCount = 0
    for frame in allFrames:
        if frame["Balls"] != None:
            if len(frame["Balls"]) > 0:
                validFrames.append(frame)
            else:
                invalidFrameCount += 1
        else:
            invalidFrameCount += 1
    print("Valid Framecount: " + str(len(validFrames)))
    print("Invalid Framecount: " + str(invalidFrameCount))


    # create batches (continuos frames with annotated balls)
    Batches = []
    for i in range(BatchSize - 1, len(allFrames)):
        batch = []
        frameNumber = 0
        for o in reversed(range(0, BatchSize)):
            frame = allFrames[i - o]
            if (o == BatchSize - 1):
                frameNumber = frame["FrameNumber"]
            if frame["FrameNumber"] == frameNumber + BatchSize - 1 - o:
                balls = frame["Balls"]
                if balls != None and len(balls) > 0:
                    batch.append(copy.deepcopy(frame))
        if (len(batch) == BatchSize):
            Batches.append(batch)

    # make batches relative
    for batch in Batches:
        prevPos = None
        for frame in batch:
            ball = frame["Balls"][0]
            if prevPos == None:
                prevPos = copy.deepcopy(ball["Position"])
                ball["Position"]["X"] = 0
                ball["Position"]["Y"] = 0
            else:
                x = ball["Position"]["X"] - prevPos["X"]
                y = ball["Position"]["Y"] - prevPos["Y"]
                prevPos = copy.deepcopy(ball["Position"])
                ball["Position"]["X"] = x
                ball["Position"]["Y"] = y


    # print some more statistics
    print("Valid Batches: " + str(len(Batches)))
    # print Batches to disk
    print("Writing Batches to: " + "./predictionBatches/Batches-" + str(fileNumber) + ".json")
    with open("./predictionBatches/Batches-" + str(fileNumber) + ".json", 'w') as outfile:
        json.dump(Batches, outfile, sort_keys=True, indent=2)
