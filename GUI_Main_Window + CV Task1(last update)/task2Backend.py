from task2Frontend import Ui_Form
from task2stereovision import DepthMap
from PyQt6.QtCore import QRunnable, Qt, QThreadPool, QObject, pyqtSignal, pyqtSlot, QPoint
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtGui import  QPixmap, QImage
import numpy as np


class StereoVision(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.points = []
        self.flag = False
        #user chooses left image
        self.img1path, _ = QFileDialog.getOpenFileName(self, "Select left image file", "", "Image Files (*.png *.jpeg *.jpg)")
        if not self.img1path:
            raise FileExistsError
        #user chooses right image
        self.img2path, _ = QFileDialog.getOpenFileName(self, "Select right image file", "", "Image Files (*.png *.jpeg *.jpg)")
        if not self.img2path:
            raise FileExistsError
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Stereo vision")

        #display original images
        self.show_images(self.convert_to_QImage(self.img1path), label=self.ui.img1_label)
        self.show_images(self.convert_to_QImage(self.img2path), label=self.ui.img2_label)

        #start stereo alogorithm for the 2 images
        self.task2 = Task2Excution(self.img1path, self.img2path)
        self.task2.images_signal.signal.connect(self.display_image)
        self.task2_threadpool = QThreadPool()
        self.task2_threadpool.start(self.task2)


    def convert_to_QImage(self, image_path):
        image = QImage(image_path)
        if image.isNull():
            return QImage()
        return image


    def show_images(self, image, label):
        #pixmap for images
        pixmap = QPixmap.fromImage(image)
        #scale image(pixmap) to fit label
        pixmap = pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation)
        #set image as new pixmap
        label.setPixmap(pixmap)   


    @pyqtSlot(QImage, QImage, QImage)    
    def display_image(self, epiimg1, epiimg2, dispmap):
        self.disp_map = dispmap
        self.flag = True
        images = [epiimg1, epiimg2, dispmap]
        labels = [self.ui.epilines1_label, self.ui.epilines2_label, self.ui.disparitymap_label]

        for image, label in zip(images, labels):
            self.show_images(image, label)


    def mousePressEvent(self, event):
        if self.flag and event.button() == Qt.MouseButton.LeftButton:
            #global position of the mouse click
            global_pos = event.globalPosition().toPoint()
            #map the global position to the disparitymap label's coordinates
            local_pos = self.ui.disparitymap_label.mapFromGlobal(global_pos)
            #check if the click is within the bounds of the label
            if self.ui.disparitymap_label.rect().contains(local_pos):
                if len(self.points) == 2:
                    self.ui.length_text.setText("")
                    self.points = []  #clear previous points
                if len(self.points) < 2:
                    self.points.append(local_pos)
                    if len(self.points) == 2:
                        length = self.task2.get_length(self.descale(self.points[:2]))  #emit points
                        self.ui.length_text.setText(f"Length = {length:.2f} cm")

        
    def descale(self, points):
        #get size of the original image
        original_size = QImage(self.disp_map).size()

        #get size of the displayed pixmap (after scaling to fit the label)
        displayed_size = self.ui.disparitymap_label.pixmap().size()

        #calculate scale factors
        scale_w = original_size.width() / displayed_size.width()
        scale_h = original_size.height() / displayed_size.height()

        #apply the scale factors to the clicked points
        original_points = [
                            QPoint(int(point.x() * scale_w), int(point.y() * scale_h))
                            for point in points
                          ]

        return original_points
      

class ImageSignal(QObject):
    signal = pyqtSignal(QImage, QImage, QImage)

    
class Task2Excution(QRunnable):
    def __init__(self, path1, path2):
        super().__init__()
        self.img1 = path1
        self.img2 = path2
        self.images_signal = ImageSignal()


    def run(self):
        #start stereo alogorithm for the 2 images
        self.task2 = DepthMap(self.img1, self.img2)

        #get result images and convert to QImage
        epiimage1 = self.convert_to_QImage(self.task2.img1_epilines)
        epiimage2 = self.convert_to_QImage(self.task2.img2_epilines)
        disparitymap = self.convert_to_QImage(self.task2.disparity_normalized)

        #emit signal to display images
        self.images_signal.signal.emit(epiimage1, epiimage2, disparitymap)


    def convert_to_QImage(self, image):
        if isinstance(image, np.ndarray):
            if len(image.shape) == 2:  #grayscale image
                height, width = image.shape
                #convert to QImage with grayscale format
                qimage = QImage(image.data, width, height, width, QImage.Format.Format_Grayscale8)
            elif len(image.shape) == 3 and image.shape[2] == 3:  #RGB image
                height, width = image.shape[:2]
                #convert to QImage with RGB format
                qimage = QImage(image.data, width, height, width * 3, QImage.Format.Format_RGB888)
            else:
                #handle other cases or invalid formats
                return QImage()
            return qimage.copy()
        return QImage()
    
    def get_length(self, points):
        return self.task2.calculate_length(points[0], points[1])

    
