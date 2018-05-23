import json
import glob
from pprint import pprint

BatchSize = 5

jsonFiles = glob.glob("../Anotations/*.json");
print("Files found: " + str(len(jsonFiles)))

allFrames = []

for file in jsonFiles:
    #print("read file: " + file)
    with open(file) as f:
        data = json.load(f)
        #print("Frames found: " + str(len(data)))
        for frame in data:
            allFrames.append(frame)

print("Total Framecount: " + str(len(allFrames)))

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


Batches = []
for i in range(BatchSize - 1, len(allFrames)):
    batch = []
    for o in reversed(range(0, BatchSize)):
        frame = allFrames[i - o]
        balls = frame["Balls"]
        if balls != None and len(balls) > 0:
            batch.append(frame)
    if (len(batch) == BatchSize):
        Batches.append(batch)


print("Valid Batches: " + str(len(Batches)))
print("Writing Batches to: " + "./Batches.json")
with open('Batches.json', 'w') as outfile:
    json.dump(Batches, outfile, sort_keys=True, indent=2)


