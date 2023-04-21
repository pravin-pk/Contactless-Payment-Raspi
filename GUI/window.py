import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtCore import pyqtSlot, QTimer, QThread, Qt

from camera import _Camera
scan = -1


# import cv2
# from roiExtraction import ROIExtractor
# import time, threading
# from threading import Thread, Lock


class LoginWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget

        username_label = QLabel("Username")
        self.username_field = QLineEdit()
        password_label = QLabel("Password")
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(username_label)
        layout.addWidget(self.username_field)
        layout.addSpacing(10)
        layout.addWidget(password_label)
        layout.addWidget(self.password_field)
        layout.addSpacing(20)
        layout.addWidget(login_button)
        layout.setObjectName("login_page")

        self.setLayout(layout)
        layout.setContentsMargins(450, 200, 450, 100)


       # Add spacer items to center login content in window
        spacer_top = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_bottom = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addSpacerItem(spacer_top)
        layout.addSpacerItem(spacer_bottom) 

    # # Create layouts
    #     vbox = QVBoxLayout()
    #     hbox1 = QHBoxLayout()
    #     hbox2 = QHBoxLayout()

    #     # Add widgets to layouts
    #     hbox1.addWidget(username_label)
    #     hbox1.addWidget(self.username_field)
    #     hbox2.addWidget(password_label)
    #     hbox2.addWidget(self.password_field)
    #     vbox.addLayout(hbox1)
    #     vbox.addLayout(hbox2)
    #     vbox.addWidget(login_button)

    #     # Add spacers to center widgets
    #     vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
    #     horizontal_spacer1 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    #     horizontal_spacer2 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
    #     vbox.addItem(vertical_spacer)
    #     vbox.addItem(horizontal_spacer1)
    #     vbox.addItem(horizontal_spacer2)

    #     # Set the main layout
    #     self.setLayout(vbox)

        # # Set the margins around the content
        # vbox.setContentsMargins(250, 50, 250, 50)

    def login(self):
        # Check if username and password are correct
        if self.username_field.text() == "admin" and self.password_field.text() == "admin":
            # Switch to home page
            self.stacked_widget.setCurrentIndex(1)


class HomePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget

        welcome_label = QLabel("Welcome to Contactless Payment!")
        welcome_label.setObjectName("headingLabel")

        process_label = QLabel("  Scan  >  Register  >  Pay")

        register_button = QPushButton(" New User")
        # register_button.setIcon(QIcon('images/new_user.png'))
        payment_button = QPushButton(" Checkout")
        # payment_button.setIcon(QIcon('images/checkout.png'))
        register_button.setObjectName('headingLabel')
        payment_button.setObjectName('headingLabel')
        register_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        payment_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        register_button.clicked.connect(lambda: self.change_page(0))
        payment_button.clicked.connect(lambda: self.change_page(1))

        v_layout = QVBoxLayout()
        v_layout.addWidget(welcome_label)
        v_layout.addSpacing(10)
        v_layout.addWidget(process_label)
        v_layout.addSpacing(30)

        h_layout = QHBoxLayout()
        h_layout.addWidget(register_button)
        h_layout.addSpacing(20)
        h_layout.addWidget(payment_button)
        v_layout.addSpacing(20)

        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)
        v_layout.setContentsMargins(100, 100, 100, 100)

    def change_page(self, data):
        global scan 
        scan = data
        self.stacked_widget.setCurrentIndex(2)


class ScanPage1(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        
        layout = QVBoxLayout()

        welcome_label = QLabel("Please place your palm on the camera")
        welcome_label.setObjectName("headingLabel")

        self.ROI_video_label = QLabel(self)
        # self.ROI_video_label.resize(300, 300)

        self.live_video_label = QLabel(self)
        # self.live_video_label.resize(300, 300)

        button1 = QPushButton('Open Camera', self)
        button1.clicked.connect(self.get_frame)

        button2 = QPushButton('Take Picture',self)
        button2.clicked.connect(self.get_roi)

        layout.addWidget(welcome_label)
        layout.addSpacing(20)
        h1_layout = QHBoxLayout()
        h1_layout.addWidget(button1)
        layout.addSpacing(20)
        h1_layout.addWidget(button2)
        layout.addSpacing(20)
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.ROI_video_label)
        h_layout.addSpacing(20)
        h_layout.addWidget(self.live_video_label)

        layout.addLayout(h1_layout)
        layout.addLayout(h_layout)
        self.setLayout(layout)
        layout.setContentsMargins(100,100,100,100)
    
    @pyqtSlot()
    def get_frame(self):
        # self.cam = Camera()
        # self.cam.get_frame()
        try:
            self.camera_thread = QThread()
            self.camera = _Camera()

            self.camera.moveToThread(self.camera_thread)
            self.camera.frame_processed.connect(self.display_frame)
            self.camera_thread.started.connect(self.camera.start_camera)
            self.camera_thread.start()
        except Exception as e:
            print(e)

    @pyqtSlot(QImage, QImage)
    def display_frame(self, roi, live):
        try:
            # print('main',threading.currentThread())
            pixmap2 = QPixmap.fromImage(live)
            self.live_video_label.setPixmap(pixmap2)
            pixmap1 = QPixmap.fromImage(roi)
            # pixmap1.scaled(300, 300, Qt.KeepAspectRatio)
            self.ROI_video_label.setPixmap(pixmap1)
        except Exception as e:
            print(e)

    @pyqtSlot()
    def get_roi(self):
        try:
            # status = self.cam.get_roi()
            status = self.camera.get_roi()
            print(f"Image saved - {status}")
            
            self.camera_thread.exit()
            if scan == 0:
                self.stacked_widget.setCurrentIndex(3)
            elif scan == 1:
                self.stacked_widget.setCurrentIndex(4)
        except Exception as ex:
            print(ex)

# class _ScanPage(QWidget):
#     def __init__(self, stacked_widget):
#         super().__init__()
#         self.stacked_widget = stacked_widget

#         layout = QVBoxLayout()

#         welcome_label = QLabel("Please place your palm on the camera")
#         welcome_label.setObjectName("headingLabel")

#         button1 = QPushButton('Open Camera', self)
#         button1.clicked.connect(self.get_frame)

#         button2 = QPushButton('Take Picture',self)
#         button2.clicked.connect(self.get_roi)

#         layout.addWidget(welcome_label)
#         layout.addSpacing(20)
#         h1_layout = QHBoxLayout()
#         h1_layout.addWidget(button1)
#         layout.addSpacing(20)
#         h1_layout.addWidget(button2)
#         layout.addSpacing(20)
#         h_layout = QHBoxLayout()
#         h_layout.addSpacing(20)

#         layout.addLayout(h1_layout)
#         layout.addLayout(h_layout)
#         self.setLayout(layout)
#         layout.setContentsMargins(100,100,100,100)
    
#     @pyqtSlot()
#     def get_frame(self):
#         self.cam = Camera()
#         self.cam.get_frame()

#     @pyqtSlot()
#     def get_roi(self):
#         try:
#             status = self.cam.get_roi()
#             print(f"Image saved - {status}")
            
#             if scan == 0:
#                 self.stacked_widget.setCurrentIndex(3)
#             elif scan == 1:
#                 self.stacked_widget.setCurrentIndex(4)
#         except Exception as ex:
#             print(ex)


class MatchPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        welcome_label = QLabel("Matching Please Wait...")
        welcome_label.setObjectName("headingLabel")

        pixmap = QPixmap("ROI.jpg")
        self.ROI_label = QLabel(self)
        # self.ROI_label.resize(250, 250)
        self.ROI_label.setPixmap(pixmap)

        layout.addWidget(welcome_label)
        layout.addSpacing(20)
        layout.addWidget(self.ROI_label)
        self.setLayout(layout)
        layout.setContentsMargins(100, 100, 100, 100)

    # def show_roi(self):
    #     pixmap = QPixmap('ROI.jpg')
    #     # Create QLabel object and set the pixmap as its content
    #     lbl = QLabel(self)
    #     lbl.setPixmap(pixmap)
    #     lbl.setGeometry(50, 200, pixmap.width(), pixmap.height())
    #     # print("Image Updated")

class RegisterPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

class MainWindow(QMainWindow):
    def __init__(self, W_width, w_height):
        super().__init__()

        self.setWindowTitle("Contactless Payment")
        self.setGeometry(0, 0, W_width, w_height)

        stacked_widget = QStackedWidget()
        login_page = LoginWindow(stacked_widget)
        home_page = HomePage(stacked_widget)
        # scan_page = ScanPage(stacked_widget)
        scan_page = ScanPage1(stacked_widget)
        # scan_page = _ScanPage(stacked_widget)
        register_page = RegisterPage(stacked_widget)
        match_page = MatchPage(stacked_widget)
        

        stacked_widget.addWidget(login_page) 
        stacked_widget.addWidget(home_page)
        stacked_widget.addWidget(scan_page)
        stacked_widget.addWidget(register_page)
        stacked_widget.addWidget(match_page)


        self.setCentralWidget(stacked_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    rect = screen.availableGeometry()

    with open('style.qss', 'r') as f:
        style = f.read()
    app.setStyleSheet(style)

    app_icon = QIcon('images/palmscan.png')
    app.setWindowIcon(app_icon)

    window = MainWindow(rect.width(),rect.height())
    window.show()
    sys.exit(app.exec_())
