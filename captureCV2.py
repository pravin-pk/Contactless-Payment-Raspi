import cv2
from picamera2 import Picamera2
import time

#cap = cv2.VideoCapture(0)
#print("Is Camera Open - ", cap.isOpened())
#ret, frame = cap.read()
#print("Frame Status - ", ret)
#print(frame)

#if ret:
#	cv2.imshow('cv2_image', frame)

#cap.release()

cam = Picamera2()
cam.start()
time.sleep(0.2)

frame = cam.capture_array("main")

img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.imwrite("image_cv2.jpg", img)


while True:
	frame = cam.capture_array("main")
	cv2.imshow("Live Stream", frame)
	if cv2.waitKey(1) == ord('q'):
		break

cv2.destroyAllWindows()
