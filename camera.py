from picamera2 import *
import time
import io
import base64

class Camera:
	def __init__(self):
		self.picam2 = Picamera2()

	def capture(self):


		self.picam2.start()
		#time.sleep(1)

		data = io.BytesIO()
		self.picam2.capture_file(data, format='jpeg')
		self.picam2.stop()
		img_str = base64.b64encode(data.getvalue()).decode()
		return img_str

