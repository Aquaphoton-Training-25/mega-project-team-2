from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtCore import QThreadPool, QRunnable, pyqtSignal, QObject, QUrl
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from Video_Stitching import process_videos
from Task1_Frontend import Ui_MainWindow

class VideoStitchingSignals(QObject):
    stitching_complete = pyqtSignal(str)

class Task1_SubWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Video Stitching')

        # Initialize media players and video widgets
        self.media_players = [None] * 3
        self.video_widgets = [None] * 3

        # Open file dialogs to select the two video files
        self.video1_path, _ = QFileDialog.getOpenFileName(self, "Select the first video file", "", "Video Files (*.mp4 *.avi *.mkv)")
        if not self.video1_path:
            print("No video file selected for video 1.")
            return

        self.video2_path, _ = QFileDialog.getOpenFileName(self, "Select the second video file", "", "Video Files (*.mp4 *.avi *.mkv)")
        if not self.video2_path:
            print("No video file selected for video 2.")
            return

        # Open a file dialog to select the output path
        self.output_path, _ = QFileDialog.getSaveFileName(self, "Select output file", "", "AVI Files (*.avi)")
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
        class VideoStitchingTask(QRunnable):
            def __init__(self, video1_path, video2_path, output_path, signals):
                super().__init__()
                self.video1_path = video1_path
                self.video2_path = video2_path
                self.output_path = output_path
                self.signals = signals

            def run(self):
                print(f"Stitching videos: {self.video1_path} and {self.video2_path}")
                ret, frame_rate = process_videos(self.video1_path, self.video2_path, self.output_path)
                if ret:
                    print(f"Stitching completed, output saved to {self.output_path}")
                    self.signals.stitching_complete.emit(self.output_path)
                else:
                    print("Video stitching failed.")

        task = VideoStitchingTask(video1_path, video2_path, output_path, self.signals)
        self.thread_pool.start(task)

    def setup_video_display(self, output_path):
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
        video_paths = [self.video1_path, self.video2_path, output_path]
        for i in range(3):
            print(f"Loading video: {video_paths[i]}")
            self.media_players[i].setSource(QUrl.fromLocalFile(video_paths[i]))
            self.media_players[i].setLoops(-1)  # Loop indefinitely
            self.media_players[i].play()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Resize video widgets to match their corresponding QLabel's
        if all(widget is not None for widget in self.video_widgets):
            self.video_widgets[0].setGeometry(self.ui.left_video.geometry())
            self.video_widgets[1].setGeometry(self.ui.right_video.geometry())
            self.video_widgets[2].setGeometry(self.ui.stitched_video.geometry())
