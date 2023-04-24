import cv2
import numpy as np
import time
from roiExtraction import ROIExtractor
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot, QMetaObject
from PyQt5.QtGui import QImage, QPixmap
# import xmlrpc.client
# conn = xmlrpc.client.ServerProxy('http://192.168.1.5:8111')
import threading
from picamera2 import Picamera2, Preview
from picamera2.previews.qt import QGlPicamera2


class _Camera(QObject):
    frame_processed = pyqtSignal(QImage, QImage)

    def __init__(self):
        super().__init__()
        #self.cap = cv2.VideoCapture(0)
        self.cap = Picamera2()
        config = self.cap.create_still_configuration({"size": (300,300), "format": 'RGB888'})
        self.cap.configure(config)

    @pyqtSlot()
    def start_camera(self):
        try:
            self.cap.start()
            while True:
                #ret, frame = self.cap.read()
                frame = self.cap.capture_array("main")
                
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.frame = ROIExtractor().extract(gray)
                

                roi = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
                roi = roi.rgbSwapped()
                live = QImage(img, gray.shape[1], gray.shape[0], QImage.Format_RGB888)
                #live = live.rgbSwapped()
                #live = QGlPicamera2(self.cap, width=350, height=350, keep_ar=False)

                self.frame_processed.emit(roi, live)
                # print('worker',threading.currentThread())
                # time.sleep(0.03)
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                 #   break

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
    cam = Camera()
    cam.get_frame()
