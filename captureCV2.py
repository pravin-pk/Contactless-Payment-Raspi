import cv2
from picamera2 import Picamera2
import time

class ProcessStream:
	def __init__(self):
		self.cam = Picamera2()
		self.cam.start()

	def process(self):
		time.sleep(0.2)

#frame = cam.capture_array("main")

#img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#cv2.imwrite("image_cv2.jpg", img)


		while True:
			frame = self.cam.capture_array("main")
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			cv2.imshow("Live Stream", frame)
			if cv2.waitKey(1) == ord('q'):
				break

		cv2.destroyAllWindows()

if __name__ == "__main__":
	ProcessStream().process()
