import serial
import time
from enum import Enum
from random import randint
from PyQt6.QtCore import QObject, pyqtSignal



class ControlType(Enum):
    MANUAL = "Manual"
    AUTONOMOUS = "Autonomous"


class Directions(Enum):
    FORWARD = 'F'
    BACKWARD = 'B'
    RIGHT = 'R'
    LEFT = 'L'
    STOP = 'S'

class Speed(Enum):
    ZERO = '0'
    LOW = '1'
    MEDIUM = '2'
    HIGH = '3'


class SerialHandler(QObject):
    #signal that will emit three pieces of data
    readings = pyqtSignal(float, float, float)

    def __init__(self, port_name=None, baud_rate=9600):
        super().__init__()
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.serial_port = None
        self.connect_serial_port()

    def connect_serial_port(self):
        for _ in range(2):
            try:
                self.serial_port = serial.Serial(self.port_name, self.baud_rate)
                time.sleep(2)  #wait for connection to establish
                break
            except serial.SerialException as error:
                print("Error opening serial port:", error, sep="\n", end="\n\n")
                time.sleep(1) 
        
    def send_signals(self, direction=None, distance=0, speed='0'):
        try:
            if direction is not None:#controlType is Manual
                """
                ##direction is a char (1 bytes)
                self.serial_port.write(direction.encode('utf-8'))
                """
                self.receive_signals()

            elif distance > 0 and speed != '0':#controlType is Autonomous
                """
                ###byteorder='little' indicates that the least significant byte is stored first
                # self.serial_port.write(distance.to_bytes(2, byteorder='little')) #integer is an int (2 bytes)
                self.serial_port.write(speed.encode('utf-8')) ##direction is a char (1 bytes)
                """
                self.receive_signals()
        except Exception:
           print("Error sending signals:", Exception, sep="\n", end="\n\n")
        

    def receive_signals(self):
        """
        new_readings = self.serial_port.readline().decode().strip()
        Ultrasonic, Current, Voltage = map(float, new_readings.split(" "))
        #Data should be sent in this order UltrasonicSensor_reading -> CurrentSensor_reading -> VoltageSensor_reading
        """
        
        ###########################
        Ultrasonic = randint(0, 50) #
        Current = randint(0, 50)  # removed later
        Voltage = randint(0, 50)  #
        ###########################
        if Ultrasonic and Current and Voltage:#validation of data received
            self.readings.emit(Ultrasonic, Current, Voltage)

    def connectivity_status(self):
         return True if self.serial_port else False
    
    def stop_connection(self):
        if self.serial_port:
            self.serial_port.close()