import cv2
import camera

img = cv2.imread("capture.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#cv2.imwrite('graded.jpg', img)

palm_detector = cv2.CascadeClassifier("./palm.xml")

edges = palm_detector.detectMultiScale(img, 1.1, 8)
print(edges)


for edge in edges:
	x,y,w,h = edge
	cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0))

cv2.imwrite('graded.jpg', img)
