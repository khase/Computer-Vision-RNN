import json
import copy
from pprint import pprint
import sys


with open("Batches.json") as f:
    batches = json.load(f)
    print(str(len(batches)) + " batches loaded")

    augmentedBatches = []

    for batch in batches:
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
        
        # print some statistics    
        print(str(len(newBatches)) + " valid batches augmented")
        augmentedBatches.extend(newBatches)
    # print some statistics    
    print(str(len(augmentedBatches)) + " total batches augmented")

    # print Batches to disk
    print("Writing Batches to: " + "./AugmentedBatches.json")
    with open('AugmentedBatches.json', 'w') as outfile:
        json.dump(augmentedBatches, outfile, sort_keys=True, indent=2)
