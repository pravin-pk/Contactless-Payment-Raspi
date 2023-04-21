from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time
import io
import base64
import socket
import cv2

class Camera:
	def __init__(self):
		self.picam2 = Picamera2()
		self.picam2.start_preview()

	def captureImage(self):

		self.picam2.start()
		#time.sleep(1)

		data = io.BytesIO()
		self.picam2.capture_file(data, format='jpeg')
		self.picam2.stop()
		#print(self.picam2.capture_metadata())
		img_str = base64.b64encode(data.getvalue()).decode()
		#self.picam2.stop()
		return img_str

	def captureVideo(self):
		video_config = self.picam2.create_video_configuration({"size": (150,150)})
		self.picam2.configure(video_config)
		encoder = H264Encoder(1000000)
		
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
			sock.connect(("192.168.1.6", 8222))
			stream = sock.makefile("wb")
			self.picam2.start_recording(encoder, FileOutput(stream))
			time.sleep(3)
			self.picam2.stop_recording()
			#output = FileOutput(stream)
			stream = "Hello World"
		return stream

	def processLive(self):
		self.picam2.start()
		while True:
			frame = self.picam2.capture_array("main")
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			#cv2.imshow("Live Stream", frame)
                        #self.picam2.start_preview()
			#if cv2.waitKey(1) == ord('q'):
			#	break
		#cv2.destroyAllWindows()
#                self.picam2.stop_preview()
		self.picam2.stop()

	def captureArray(self):
		#capture_config = self.picam2.create_still_configuration()
		#self.picam2.start(show_preview=False)
		print("before cam")
		array = self.picam2.switch_mode_and_capture_array("main")
		print("after cam")
#		self.picam2.start_preview()
#		time.sleep(5)
#		self.picam2.stop_preview()
		#array = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
		print(type(array))
		self.picam2.stop()
		return array



if __name__ == "__main__":
    cam = Camera()
    cam.captureArray()
