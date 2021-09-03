import cv2
import numpy as np
import serial
import time
cap = cv2.VideoCapture('output02.avi')
ser = serial.Serial("COM1", 9600, timeout=5)
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (600, 600)) # resize the output frame to be 600*600
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # apply HSV method to extract a colored object
    green_lower = np.array([10, 180, 20], np.uint8) # lower range of the green
    green_upper = np.array([180, 255, 255], np.uint8) # upper range of the green
    mask = cv2.inRange(hsv, green_lower, green_upper) # create mask in range of the lower and upper green
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)#sort contours regions
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # draw rectangle
        text = "x = " + str(x) + "y = " + str(y) # text of x and y positions
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 0, 255)) # put text above the rectangle
        # ////////////////////////////////////////////////////////////////////
        medium_x = int((x + x + w) / 2) # x at centre of rectangle
        medium_y = int((y + y + h) / 2) # y at centre of rectangle
        # ////////////////////////////////////////////////////////////////////
        cv2.line(frame, (medium_x, 0), (medium_x, 600), (0, 255, 0), 2) # draw the horizontal line

        text2 = "mediumX = " + str(medium_x)  # x-position text of centre of the rectangle
        cv2.putText(frame, text2, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.50,
                 (0, 255, 50))  # put text to appear in the frame
        # ////////////////////////////////////////////////////////////////////
        cv2.line(frame, (0, medium_y), (600, medium_y), (0, 255, 0), 2)  # draw the vertical line
        text3 = "mediumY = " + str(medium_y)  # y-position text of centre of the rectangle
        cv2.putText(frame, text3, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 255, 50))  # put text to appear in the frame
        # ////////////////////////////////////////////////////////////////////
        if (medium_x < 150) & (medium_y > 550):  # range for first valve
        ser.write(('a').encode('utf-8'))
        if (medium_x > 210) & (medium_x < 280) & (medium_y > 550):  # range for second valve
        ser.write(('b').encode('utf-8'))
        if (medium_x > 290) & (medium_x < 380) & (medium_y > 550):  # range for third valve
        ser.write(('c').encode('utf-8'))
        if (medium_x > 390) & (medium_y > 550):  # range for fourth valve
        ser.write(('d').encode('utf-8'))
        if (medium_y < 550):  # outside the required ranges
        ser.write(('e').encode('utf-8'))
        break
    cv2.imshow("frame", frame)
    key = cv2.waitKey(300)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
