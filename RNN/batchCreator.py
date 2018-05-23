import json
import glob
from pprint import pprint

BatchSize = 5

jsonFiles = glob.glob("../Anotations/*.json");
print("Files found: " + str(len(jsonFiles)))

allFrames = []

# collect all frames from annotations
for file in jsonFiles:
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
                batch.append(frame)
    if (len(batch) == BatchSize):
        Batches.append(batch)

# print some more statistics
print("Valid Batches: " + str(len(Batches)))
# print Batches to disk
print("Writing Batches to: " + "./Batches.json")
with open('Batches.json', 'w') as outfile:
    json.dump(Batches, outfile, sort_keys=True, indent=2)


