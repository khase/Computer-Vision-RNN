import cv2
import glob
import os
import re
import time

test = glob.glob("../Videos/Training-5.mp4")
print(test)
for file in test:

    #testArray = [int(s) for s in re.findall(r'\d+', file.split('\\')[1])]
    vidcap = cv2.VideoCapture(file)
    success,image = vidcap.read()
    count = 0
    success = True
    while success:
      #directory = "video" + str(testArray[0]) + "_images"
      directory = "video5_images"
      if not os.path.exists(directory):
        os.makedirs(directory)
      cv2.imwrite(directory+"/frame%d.jpg" % count, image)     # save frame as JPEG file
      success,image = vidcap.read()
      print('Read a new frame: ', success)
      time.sleep(0.05)
      count += 1
    print(count)
