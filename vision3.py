import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import random as rng
import keras
kerasNet = keras.models.load_model('kerasModel.h5')

frameWidth = 200
frameHeight = 200
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

kernel = np.ones((3,3), np.uint8)

def thresh_callback():
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    img2 = img
    ret, thresh = cv2.threshold(cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY), 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    thresh = cv2.blur(thresh, (3, 3))
    cv2.imshow('thresh',thresh)
    
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    eligible = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w > 150 and h > 200 and w < 200 and h < 325:
            eligible.append([x, y, w, h])
    
    for maybe in eligible:
        x = maybe[0]
        y = maybe[1]
        w = maybe[2]
        h = maybe[3]
        extract = img_rgb[x:x+w, y:y+h]
        try:
            cv2.imshow('extract', extract)
        except:
            print('pass2')
            pass
        try:
            extract = cv2.resize(extract, (200,200))
        except:
            print('pass3')
            pass
        
        try:
            extract = extract / 255
        except:
            print('pass4')
            pass
        try:
            extract = np.reshape(extract, [1, 200, 200, 3])
        except:
            print('pass5')
            pass

        try:
            answer = kerasNet.predict(extract)
        except:
            print('pass6')
            pass
        try:
            answer = answer[0][0]
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            if(round(answer) == 1):
                cv2.putText(img, 'Not Can: ' + str(round(answer*100, 2)) + '%', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if(round(answer) == 0):
                cv2.putText(img, 'Can: ' + str(round((1-answer)*100, 2)) + '%', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        except:
            print('pass7')
            pass

    cv2.imshow('Contours', img)
    # Convert to uint8
    #out = 255*(out.astype(np.uint8))
    #cv2.imshow('Contours', out)
    # cv2.imshow('death',threshed_img)

while cap.isOpened():
    success, img = cap.read()
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img_gray = cv2.blur(img_gray, (3,3))
    source_window = 'Source'
    cv2.namedWindow(source_window)
    cv2.imshow(source_window, img)
    # cv2.createTrackbar('Canny thresh:', source_window, thresh, max_thresh, thresh_callback)
    thresh_callback()

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

