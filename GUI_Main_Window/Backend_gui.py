from Frontend_gui import Ui_MainWindow
from SerialHandler import SerialHandler, ControlType, Directions, Speed
from CameraFeed import CameraFeed
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QThreadPool, pyqtSlot
from PyQt6.QtGui import QPixmap, QImage


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow=self)

        #initialize Serial Handler to establish connection
        self.serial_handler = SerialHandler(port_name="Bluetooth_COM_port", baud_rate=9600)
        self.serial_handler.readings.connect(self.update_readings)

        #update connectivity indicators
        self.update_connectivity_status()

        #connect signals
        self.ui.Autonomous_Button.clicked.connect(self.set_autonomous_controller)
        self.ui.Manual_Button.clicked.connect(self.set_manual_control)
        
        #creating a seperate thread for the camera feed
        self.camera_feed = CameraFeed()
        self.camera_feed.video_signal.current_frame.connect(self.update_camera_feed)#connecting QImage signal
        self.camera_feed_threadpool = QThreadPool()
        self.camera_feed_threadpool.start(self.camera_feed)#start thread

        #connect signals for screenshot button
        self.ui.ScreenShot.clicked.connect(self.screenshot_clicked)
       
    
        self.show()
        
    
    def set_autonomous_controller(self):
        ###############################
        print("Autonomous control ON")# removed later
        ###############################
        self.enable_buttons(control_type=ControlType.AUTONOMOUS, enable=True) #enable promt for speed and distance (autonomous buttons)
        self.enable_buttons(control_type=ControlType.MANUAL, enable=False)#disable forward, backward, right, and left buttons (manual buttons)
        
        self.start_autonomous_controller()#function to autonomously control the robot
        

    def set_manual_control(self):
        ###########################
        print("Manual control ON")# removed later
        ###########################
        self.enable_buttons(control_type=ControlType.MANUAL, enable=True) #enable forward, backward, right, and left buttons (manual buttons)
        self.enable_buttons(control_type=ControlType.AUTONOMOUS, enable=False) #disable promt for speed and distance (autonomous buttons)

        self.start_manual_controller() #function to manually control the robot

    
    def enable_buttons(self, control_type, enable :bool):
            manual_buttons = [self.ui.Forwrd_Button, self.ui.Backward_Button,
                            self.ui.Right_Button, self.ui.Left_Button]
            
            autonomous_buttons = [self.ui.LowSpeed_Button, self.ui.MediumSpeed_Button,
                                self.ui.HighSpeed_Button, self.ui.Distance_Edit]

            if control_type.value == "Manual":
                for button in manual_buttons:
                    button.setEnabled(enable) 
                self.ui.Manual_Button.setEnabled(not enable)
                
            elif control_type.value == "Autonomous":
                for button in autonomous_buttons:
                    button.setEnabled(enable) 
                self.ui.Autonomous_Button.setEnabled(not enable)

  
    def start_autonomous_controller(self):
        self.set_direction(Directions.FORWARD)
        self.set_speed(Speed.ZERO) #speed initially set to zero

        #connect Signals
        self.ui.LowSpeed_Button.clicked.connect(lambda: self.set_speed(speed=Speed.LOW))
        self.ui.MediumSpeed_Button.clicked.connect(lambda: self.set_speed(speed=Speed.MEDIUM))
        self.ui.HighSpeed_Button.clicked.connect(lambda: self.set_speed(speed=Speed.HIGH))
        self.ui.Distance_Edit.returnPressed.connect(self.send_autonomous_signal) #input distance + enter


    def start_manual_controller(self):
        self.set_direction(Directions.STOP) #no direction initially
        self.set_speed(Speed.MEDIUM) #speed alwyas medium at manual mode
        
        #connect signals while button pressed to MOVE
        self.ui.Forwrd_Button.pressed.connect(lambda: self.send_manual_signal(Directions.FORWARD))
        self.ui.Backward_Button.pressed.connect(lambda: self.send_manual_signal(Directions.BACKWARD)) 
        self.ui.Right_Button.pressed.connect(lambda: self.send_manual_signal(Directions.RIGHT))
        self.ui.Left_Button.pressed.connect(lambda: self.send_manual_signal(Directions.LEFT))

        #connect signals when button released to STOP
        self.ui.Forwrd_Button.released.connect(lambda: self.send_manual_signal(Directions.STOP))
        self.ui.Backward_Button.released.connect(lambda: self.send_manual_signal(Directions.STOP))
        self.ui.Right_Button.released.connect(lambda: self.send_manual_signal(Directions.STOP))
        self.ui.Left_Button.released.connect(lambda: self.send_manual_signal(Directions.STOP))
         
    
    def send_autonomous_signal(self):
        try:
            distance = int(self.ui.Distance_Edit.text())
            if distance > 0:
                self.serial_handler.send_signals(distance=distance, speed=self.current_speed)
            else: return
        except ValueError: return


    def send_manual_signal(self, direction):
        self.set_direction(direction) 
        self.serial_handler.send_signals(direction=self.current_direction)


    def set_speed(self, speed):
        self.current_speed = speed.value

    def set_direction(self, direction):
        self.current_direction = direction.value
                


    def update_readings(self, Ultrasonic, current, voltage):#called when signal is emmited
        #update signals received from arduino
        self.ui.Sonar.setText(f'{Ultrasonic}m')
        self.ui.Current.setText(f'{current}A')
        self.ui.Voltage.setText(f'{voltage}V')

        #update direction indicators
        self.update_direction_status()
        #update speed indicators
        self.update_speed_status()
        #update connectivity indicators
        self.update_connectivity_status()


    def update_direction_status(self):
        match self.current_direction:
            case "F":
                self.ui.Direction.setText("Forward")
            case "B":
                self.ui.Direction.setText("Backward")
            case "R":
                self.ui.Direction.setText("Right")
            case "L":
                self.ui.Direction.setText("Left")
            case _:
                self.ui.Direction.setText("Stop")


    def update_speed_status(self):
        match self.current_speed:
            case '1':
                self.ui.Speed.setText("Low")
            case '2':
                self.ui.Speed.setText("Medium")
            case '3':
                self.ui.Speed.setText("High")


    def update_connectivity_status(self):
        color = "green" if self.serial_handler.connectivity_status() else "red"
        self.ui.connectivity_indicator.setStyleSheet(f"border-radius: 10px;\nbackground-color: {color};")


    @pyqtSlot(QImage)
    def update_camera_feed(self, image):

        pixmap = QPixmap.fromImage(image)
        self.ui.CameraFeed.setPixmap(pixmap)


    def closeEvent(self, event):
        #end bluetooth connection with MCU
        self.serial_handler.stop_connection()
        #stop the camera feed
        self.camera_feed.stop()
        #ensure the thread has finished
        self.camera_feed_threadpool.waitForDone()


    def screenshot_clicked(self):
        self.camera_feed.capture_screenshot()

        


if __name__ == '__main__':
    app = QApplication([])
    ex = MainWindow()
    app.exec()