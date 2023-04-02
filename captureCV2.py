import cv2

cap = cv2.VideoCapture(-1)

ret, frame = cap.read()
print(ret)

if ret:
	cv2.imwrite('cv2_image.jpg', frame)

cap.release()
