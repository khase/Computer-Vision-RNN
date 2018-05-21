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
    #success,image = vidcap.read()
    count = 0
    #success = True

    framecount = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

    frames = 0
    while frames < framecount:
        ret, img = vidcap.read()
        frames += 1
        if (type(img) == type(None)):
            break
        directory = "video5_images"
        if not os.path.exists(directory):
          os.makedirs(directory)
        cv2.imwrite(directory+"/frame%d.jpg" % count, img)     # save frame as JPEG file
        print('Read a new frame: ', ret)
        time.sleep(0.05)
        count += 1
        #if (0xFF & cv2.waitKey(5) == 27) or img.size == 0:
        #    break
    print(count)
