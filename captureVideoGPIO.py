import RPi.GPIO as gpio
import time
import xmlrpc.client
from camera import Camera

trigPin = 23
outPin = 11

gpio.setmode(gpio.BCM)
gpio.setup(trigPin, gpio.IN, pull_up_down=gpio.PUD_DOWN)
#gpio.setup(trigPin, gpio.IN)
#gpio.setup(outPin, gpio.OUT)

conn = xmlrpc.client.ServerProxy('http://192.168.1.5:8111')
cam = Camera()
try:
	while 1:
		if gpio.input(trigPin)==gpio.HIGH:
			image = cam.capture()

			status = conn.saveImage(image)
			print("Triggerd", status)
			continue
		else:
			print("Not Triggered")

		time.sleep(1)
except KeyboardInterrupt:
	gpio.cleanup()
