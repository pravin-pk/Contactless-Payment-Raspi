import RPi.GPIO as gpio
import time
import xmlrpc.client
from camera import Camera
import cv2

capturePin = 23
videoPin = 24

gpio.setmode(gpio.BCM)
gpio.setup(capturePin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(videoPin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
#gpio.setup(outPin, gpio.OUT)

conn = xmlrpc.client.ServerProxy('http://192.168.137.128:8111')
cam = Camera()
try:
	while 1:
		if gpio.input(capturePin)==gpio.HIGH:
			image = cam.captureImage()

			status = conn.saveImage(image)
			print("Image transferred to server - ", status)
			continue
		elif gpio.input(videoPin)==gpio.HIGH:
			video = cam.captureVideo()
			#status = conn.saveVideo(video)
			print(type(video))
#			cv2.imshow("stream",video.outputframe)
			print("Video transferred to server - ")
			continue
		else:
			print("Not Triggered")

		time.sleep(1)
except KeyboardInterrupt:
	gpio.cleanup()
