
import cv2
import numpy as np
import time
from roiExtraction import ROIExtractor
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot, QMetaObject
from PyQt5.QtGui import QImage, QPixmap
# import xmlrpc.client
# conn = xmlrpc.client.ServerProxy('http://192.168.1.5:8111')
import threading
import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
from libcamera import controls

capturePin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(capturePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class _Camera(QObject):
    frame_processed = pyqtSignal(QImage, QImage)

    def __init__(self):
        super().__init__()
        #self.cap = cv2.VideoCapture(0)
        self.cap = Picamera2()
        config = self.cap.create_still_configuration({"size": (500,500), "format": 'RGB888'})
        self.cap.configure(config)
        self.cap.set_controls({"AfMode": controls.AfModeEnum.Continuous})

    @pyqtSlot()
    def start_camera(self):
        try:
            self.cap.start()
            while True:
                #ret, frame = self.cap.read()
                if GPIO.input(capturePin)!=GPIO.HIGH:
                    frame = self.cap.capture_array("main")

                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = cv2.rectangle(img, (100,100),(400,400),(0,255,0),2)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    self.frame = ROIExtractor().extract(gray)
                else:
                    self.frame = np.zeros((150, 150))
                    img = np.zeros((150, 150))


                roi = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
                #roi = roi.rgbSwapped()
                live = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
                #live = live.rgbSwapped()
                #live = QGlPicamera2(self.cap, width=350, height=350, keep_ar=False)


                self.frame_processed.emit(roi, live) 
                # print('worker',threading.currentThread())

        except Exception as ex:
            print(ex)

        #self.cap.release()
        self.cap.stop()
        # cv2.destroyAllWindows()
        return

    def get_live(self):
        _, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
    
    def get_roi(self):

        return cv2.imwrite("ROI.jpg", self.frame)

    def __del__(self):
        self.cap.stop()

    


if __name__ == '__main__':
    cam = _Camera()
    cam.get_frame()
