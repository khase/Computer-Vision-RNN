import cv2
import glob
import os
import re

#test = glob.glob("../Videos/*.mp4")
#print(test)
#for file in test:
file = 'video0.avi'
#testArray = [int(s) for s in re.findall(r'\d+', file.split('\\')[1])]
vidcap = cv2.VideoCapture(file)
success,image = vidcap.read()
count = 0
success = True
while success:
  directory = "video0_images"
  if not os.path.exists(directory):
    os.makedirs(directory)
  cv2.imwrite(directory+"/frame%d.jpg" % count, image)     # save frame as JPEG file
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1
