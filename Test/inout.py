import sys
import glob
import json
from pprint import pprint
import tensorflow as tf

inputdir = "..\\Anotations"

for file in glob.glob("../Anotations/video5_images.txt"):
    print(file)
    with open(inputdir + "\\" + file) as f:
        data = json.load(f)

    input = []
    output = []
    index = 0
    for frame in data:
        if index > 0:
            output.append(frame["balls"])
            input.append(lastframe["balls"])

        lastframe = frame;
        index += 1

    print("input:")
    pprint(input)
    print("output:")
    pprint(output)
