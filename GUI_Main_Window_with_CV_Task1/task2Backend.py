from task2Frontend import Ui_Form
from task2stereovision import DepthMap
from PyQt6.QtCore import QRunnable, Qt, QThreadPool
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap, QImage
import numpy as np


class StereoVision(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Stereo vision")

        #user chooses left image
        self.img1path, _ = QFileDialog.getOpenFileName(self, "Select left image file", "", "Image Files (*.png *.jpeg *.jpg)")
        if not self.img1path:
            return
        #user chooses right image
        self.img2path, _ = QFileDialog.getOpenFileName(self, "Select right image file", "", "Image Files (*.png *.jpeg *.jpg)")
        if not self.img2path:
            return
        
        self.stereo_vision = RunTask(self.img1path, self.img2path, self.ui)
        self.stereo_vision_threadpool = QThreadPool()
        self.stereo_vision_threadpool.start(self.stereo_vision)

        self.show()


class RunTask(QRunnable):
    def __init__(self, path1, path2, window):
        super().__init__()
        self.img1path = path1
        self.img2path = path2
        self.window = window


    def run(self):
        #display original images
        self.show_image(self.img1path, self.window.img1_label)
        self.show_image(self.img2path, self.window.img2_label)

        self.task2 = DepthMap(self.img1path, self.img2path)

        #get images with epilines
        self.img1_epilines, self.img2_epilines = self.task2.draw_epipolar_lines()
        #display images with epipolar lines
        self.show_image(self.img1_epilines, self.window.epilines1_label)
        self.show_image(self.img2_epilines, self.window.epilines2_label)

        #get disparity map
        self.disparity_map =  self.task2.get_disparity_map()
       
        #display disparity map
        self.show_image(self.disparity_map, self.window.disparitymap_label)
        


    def show_image(self, image, label):
        if isinstance(image, np.ndarray):
            height, width = image.shape[:2]
            image = QImage(image.data, width, height, width * 3, QImage.Format.Format_RGB888)
        else:
            image = QImage(image)
            
        #pixmap for images
        pixmap = QPixmap.fromImage(image)
        #scale image(pixmap) to fit label
        pixmap = pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation)
        #set image as new pixmap
        label.setPixmap(pixmap)
        
        
        
        
