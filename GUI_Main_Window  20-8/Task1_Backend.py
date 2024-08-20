from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QFileDialog,QApplication
from PyQt6.QtCore import QThreadPool, QRunnable, pyqtSignal, QObject, QUrl
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from Video_Stitching import Video_Stitching
from Task1_Frontend import Ui_MainWindow
import time
import tkinter as tk
from tkinter import filedialog
import easygui
                
class VideoStitchingSignals(QObject):
    stitching_complete = pyqtSignal()

class Task1_SubWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Video Stitching')
        
        # Initialize media players and video widgets
        self.media_players = [None] * 3
        self.video_widgets = [None] * 3
        #self.show()
        # Open file dialogs to select the two video files
        
        
        self.video1_path, _ = QFileDialog.getOpenFileName(self)
        #self.video1_path=r'C:\Users\HP ENVY\Downloads\Right(Better Quality).mp4'
        if not self.video1_path:
            print("No video file selected for video 1.")
            return
        
        

        self.video2_path, _ = QFileDialog.getOpenFileName(self)
        #self.video2_path=r'C:\Users\HP ENVY\Downloads\Left (Better Quality).mp4'
        if not self.video2_path:
            print("No video file selected for video 2.")
            return

        # Open a file dialog to select the output path
        
        self.output_path, _ = QFileDialog.getSaveFileName(self)
        #self.output_path=r'C:\Users\HP ENVY\Downloads\stitched (Higher Quality).avi'
        if not self.output_path:
            print("No output file selected.")
            return

        # Initialize QThreadPool and signals
        self.thread_pool = QThreadPool()
        self.signals = VideoStitchingSignals()
        self.signals.stitching_complete.connect(self.setup_video_display)

        # Start video stitching task
        self.start_video_stitching(self.video1_path, self.video2_path, self.output_path)

    def start_video_stitching(self, video1_path, video2_path, output_path):
        

        task = Video_Stitching(video1_path, video2_path, output_path, self.signals)
        self.thread_pool.start(task)

    def setup_video_display(self):
        #time.sleep(10)
        print("Setting up video display...")
        # Initialize media players and video widgets if not already done
        if any(widget is None for widget in self.video_widgets):
            self.video_widgets = [QVideoWidget(self) for _ in range(3)]
            self.media_players = [QMediaPlayer(self) for _ in range(3)]

            # Set the video widgets' geometry to match the QLabel's
            self.video_widgets[0].setGeometry(self.ui.left_video.geometry())
            self.video_widgets[1].setGeometry(self.ui.right_video.geometry())
            self.video_widgets[2].setGeometry(self.ui.stitched_video.geometry())

            # Set each media player's output to its corresponding video widget
            for i in range(3):
                self.media_players[i].setVideoOutput(self.video_widgets[i])
                self.video_widgets[i].show()  # Make video widgets visible

        # Load and play the videos
        video_paths = [self.video1_path, self.video2_path,self.output_path]
        for i in range(3):
            print(f"Loading video: {video_paths[i]}")
            self.media_players[i].setSource(QUrl.fromLocalFile(video_paths[i]))
            self.media_players[i].setLoops(-1)  # Loop indefinitely
            self.media_players[i].play()
'''
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Resize video widgets to match their corresponding QLabel's
        if all(widget is not None for widget in self.video_widgets):
            self.video_widgets[0].setGeometry(self.ui.left_video.geometry())
            self.video_widgets[1].setGeometry(self.ui.right_video.geometry())
            self.video_widgets[2].setGeometry(self.ui.stitched_video.geometry())
'''
    
if __name__ == '__main__':
    app = QApplication([])
    ex = Task1_SubWindow()
    ex.show()
    app.exec()   