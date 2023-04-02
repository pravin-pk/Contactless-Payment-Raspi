from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time
import io
import base64
import socket

class Camera:
	def __init__(self):
		self.picam2 = Picamera2()

	def captureImage(self):


		self.picam2.start()
		#time.sleep(1)

		data = io.BytesIO()
		self.picam2.capture_file(data, format='jpeg')
		self.picam2.stop()
		#print(self.picam2.capture_metadata())
		img_str = base64.b64encode(data.getvalue()).decode()
		return img_str

	def captureVideo(self):
		video_config = self.picam2.create_video_configuration()
		self.picam2.configure(video_config)
		encoder = H264Encoder(1000000)
		
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
			sock.connect(("192.168.1.5", 8222))
			stream = sock.makefile("wb")
			self.picam2.start_recording(encoder, FileOutput(stream))
			time.sleep(3)
			self.picam2.stop_recording()
		return "done"
