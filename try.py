import cv2
import numpy as np
import time
from roiExtraction import ROIExtractor
import xmlrpc.client

cap = cv2.VideoCapture(0)
conn = xmlrpc.client.ServerProxy('http://192.168.1.5:8111')


while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = frame

    # hands = hand_cascade.detectMultiScale(gray, 1.3, 5)

    # for (x, y, w, h) in hands:
    #     cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0))

    # if len(hands) > 0:
    #     frame = ROIExtractor().extract(gray)
    # else:
    #     frame = np.zeros((350,350,3), np.uint8)

    frame = ROIExtractor().extract(gray)
    status = conn.saveImage(frame)
    print(status)
    time.sleep(1)

    # cv2.namedWindow("Hand Palm Detection", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("Hand Palm Detection", 200, 200)
   # cv2.imshow('Hand Palm Detected', frame)
    #cv2.imshow('Live feedback', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        # cv2.imwrite('ROI_extracted.jpg',frame)
        break

cap.release()
#cv2.destroyAllWindows()
