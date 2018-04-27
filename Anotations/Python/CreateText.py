import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import glob
import re

def sort_human(l):

  convert = lambda text: int(text) if text.isdigit() else text
  alphanum = lambda key: [ convert(c) for c in re.findall(r'\d+', key.split('\\')[1]) ]
  l.sort( key=alphanum )
  print(l)
  return l


# Root directory of the project
ROOT_DIR = os.path.abspath("../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
import coco

#%matplotlib inline

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "images")

class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    DETECTION_MIN_CONFIDENCE = 0.4

config = InferenceConfig()
config.display()

# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)
# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']

subdirs = glob.glob("*images")
#subdirs = sort_human(subdirs)
for filename in subdirs:
    directory = filename
    frames = glob.glob(filename + "/*.jpg")
    frames = sort_human(frames)
    file = open(filename + ".txt","w")
    file.write('[\n')
    j = 0
    for frameName in frames:
        print(frameName)
        image = skimage.io.imread(frameName)

        # Run detection
        results = model.detect([image], verbose=0)
        testArray = [int(s) for s in re.findall(r'\d+', frameName.split('\\')[1])]

        # Visualize results
        r = results[0]
        if j > 0:
            file.write(",\n")
        file.write("\t{")
        file.write('\n\t\t"frameNumber": ' + str(testArray[0]) +',\n')
        file.write('\t\t"balls":\n')
        file.write('\t\t[\n')
        i = 0
        for roi in r['rois']:
            if r['class_ids'][i] == 60:
                continue
            if i > 0:
                file.write(',')
            file.write('\n\t\t\t{\n')
            y = int(round((roi[0]+roi[2])/2))
            x = int(round((roi[1]+roi[3])/2))
            height = roi[2]-roi[0]
            width = roi[3]-roi[1]

            file.write('\t\t\t\t"tag": ' + str(i) + ",\n")
            file.write('\t\t\t\t"position": {"x": ' + str(x) + ', "y": ' + str(y) +"},\n")
            file.write('\t\t\t\t"boundingBox": {"width": ' + str(width) + ', "height": ' + str(height) +"}\n")

            i = i + 1
            file.write('\t\t\t}')

        j = j + 1
        file.write('\n\t\t]\n')
        file.write('\t}')

    file.write(']')
    file.close()
'''
        file = open(frameName,"w")

        file.write(“Hello World”)
        file.write(“This is our new text file”)
        file.write(“and this is another line.”)
        file.write(“Why? Because we can.”)

        file.close()
        vidcap = cv2.VideoCapture(file)
        success,image = vidcap.read()
        count = 0
        success = True
        while success:
          if not os.path.exists(file + "folder"):
            os.makedirs(file + "folder")
          cv2.imwrite(file + "folder"+"/frame%d.jpg" % count, image)     # save frame as JPEG file
          success,image = vidcap.read()
          print('Read a new frame: ', success)
          count += 1

# Load a random image from the images folder
file_names = next(os.walk(IMAGE_DIR))[2]

filename = os.path.join(IMAGE_DIR, 'vlc1.png')

#image = skimage.io.imread(os.path.join(IMAGE_DIR, random.choice(file_names)))
'''
