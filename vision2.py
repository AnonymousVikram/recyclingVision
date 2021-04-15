import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import random as rng
#import keras

# kerasNet = keras.models.load_model('/Users/anonymousvikram/Downloads/model18.h5')

frameWidth = 200
frameHeight = 200
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

kernel = np.ones((3,3), np.uint8)

def thresh_callback(val):
    threshold = val
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    img2 = img
    ret, threshed_img = cv2.threshold(cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY),
                127, 255, cv2.THRESH_OTSU)
    
    vals = []
    
    contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    # img2 = img
    # img2 = cv2.drawContours(img2, contours, -1, (0,255,0), 3)
    # cv2.imshow('i hate my life',img2)

    for c in contours:
        # get the bounding rect
        x, y, w, h = cv2.boundingRect(c)
        # draw a green rectangle to visualize the bounding rect
        if(w > 100 and h > 100 and w < 400):
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # get the min area rect
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            # convert all coordinates floating point values to int
            box = np.int0(box)
            # draw a red 'nghien' rectangle
            cv2.drawContours(img, [box], 0, (0, 0, 255))

            # finally, get the min enclosing circle
            # (x, y), radius = cv2.minEnclosingCircle(c)
            # convert all values to int
            # center = (int(x), int(y))
            # radius = int(radius)
            # and draw the circle in blue
            # img = cv2.circle(img, center, radius, (255, 0, 0), 2)

    print(len(contours))
    # cv2.drawContours(img, contours, -1, (255, 255, 0), 1)
    cv2.imshow('Contours', img)
    cv2.imshow('death',threshed_img)

while cap.isOpened():
    success, img = cap.read()
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img_gray = cv2.blur(img_gray, (3,3))
    source_window = 'Source'
    cv2.namedWindow(source_window)
    cv2.imshow(source_window, img)
    max_thresh = 255
    thresh = 100 # initial threshold
    cv2.createTrackbar('Canny thresh:', source_window, thresh, max_thresh, thresh_callback)
    thresh_callback(thresh)

    #img2 = cv2.resize(img, (200, 200))
    #img2 = img2/255
    #img2 = np.reshape(img2, [1, 200, 200, 3])
    
    #prediction = kerasNet.predict(img2)
    #prediction = prediction[0][0]
    #answer = round(prediction)
    
    #if answer == 0:
     #   print("Prediction: Can")
      #  print("Confidence:", str(round(((1-prediction) * 100), 2)) + "%")
    #if answer == 1:
     #   print("Prediction: Not Can")
      #  print("Confidence:", str(round(((prediction) * 100), 2)) + "%")
    #cv2.imshow("frame", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(1.0/15)
cap.release()
cv2.destroyAllWindows()

