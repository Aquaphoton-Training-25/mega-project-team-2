import cv2
from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, QMutex, QMutexLocker
from PyQt6.QtGui import QImage
import time

class CameraFeedSignals(QObject):
    #frame signal, sent to the main thread
    current_frame = pyqtSignal(QImage)


class CameraFeed(QRunnable):
    def __init__(self):
        super().__init__()
        self.video_signal = CameraFeedSignals()
        self.running_state = True  #flag to control the running state
        self.pic_number = 0
        self.frame = None
        self.screenshoot_frame = None


    def run(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  

        if not cap.isOpened():
            print("Error: Unable to access the camera.")
            return
        
        while cap.isOpened() and  self.running_state:
            ret, self.frame = cap.read() #ret indicates success
            if ret:
                #flip the frame horizontally to overcome selfi camera mirror
                self.frame = cv2.flip(self.frame, 1)
                self.screenshoot_frame = self.frame

                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) #convert the image from openCv format (BGR) to Qt format (RGB)
                height, width, channels = self.frame.shape
                bytes_per_line = channels*width
                image = QImage(self.frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)

                #emit the frame as a QImage to the main thread
                self.video_signal.current_frame.emit(image)

            else: break
        cap.release()


    def capture_screenshot(self):
        if self.screenshoot_frame is not None:
            self.pic_number +=1
            cv2.imwrite(f"screenshots/screenshoot{self.pic_number}.jpg", self.screenshoot_frame)    

    
    def stop(self):
        self.running_state = False

    
        

    