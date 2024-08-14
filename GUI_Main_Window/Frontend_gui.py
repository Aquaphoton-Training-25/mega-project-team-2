# Form implementation generated from reading ui file 'RemoteCar.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(643, 436)
        font = QtGui.QFont()
        font.setBold(False)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 57)")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Manual_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Manual_Button.setGeometry(QtCore.QRect(360, 270, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.Manual_Button.setFont(font)
        self.Manual_Button.setStyleSheet("background-color: rgb(0, 0, 255);\n"
"")
        self.Manual_Button.setObjectName("Manual_Button")
        self.Autonomous_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Autonomous_Button.setGeometry(QtCore.QRect(360, 150, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.Autonomous_Button.setFont(font)
        self.Autonomous_Button.setStyleSheet("background-color: rgb(0, 0, 255);\n"
"")
        self.Autonomous_Button.setObjectName("Autonomous_Button")
        self.CameraFeed = QtWidgets.QLabel(parent=self.centralwidget)
        self.CameraFeed.setGeometry(QtCore.QRect(10, 30, 320, 240))
        self.CameraFeed.setStyleSheet("background-color: #FFFFFF;")
        self.CameraFeed.setText("")
        self.CameraFeed.setObjectName("CameraFeed")
        self.ScreenShot = QtWidgets.QPushButton(parent=self.centralwidget)
        self.ScreenShot.setGeometry(QtCore.QRect(10, 280, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.ScreenShot.setFont(font)
        self.ScreenShot.setStyleSheet("background-color: rgb(0, 0, 255);\n"
"\n"
"")
        self.ScreenShot.setFlat(False)
        self.ScreenShot.setObjectName("ScreenShot")
        self.CV_task1 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.CV_task1.setGeometry(QtCore.QRect(360, 30, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.CV_task1.setFont(font)
        self.CV_task1.setStyleSheet("background-color: rgb(0, 0, 255);\n"
"")
        self.CV_task1.setObjectName("CV_task1")
        self.CV_task2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.CV_task2.setGeometry(QtCore.QRect(360, 80, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.CV_task2.setFont(font)
        self.CV_task2.setStyleSheet("background-color: rgb(0, 0, 255);\n"
"")
        self.CV_task2.setObjectName("CV_task2")
        self.Sonar = QtWidgets.QLabel(parent=self.centralwidget)
        self.Sonar.setGeometry(QtCore.QRect(10, 350, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Sonar.setFont(font)
        self.Sonar.setStyleSheet("background-color: rgb(170, 255, 255);\n"
"")
        self.Sonar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Sonar.setObjectName("Sonar")
        self.Voltage = QtWidgets.QLabel(parent=self.centralwidget)
        self.Voltage.setGeometry(QtCore.QRect(170, 350, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Voltage.setFont(font)
        self.Voltage.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.Voltage.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Voltage.setObjectName("Voltage")
        self.Current = QtWidgets.QLabel(parent=self.centralwidget)
        self.Current.setGeometry(QtCore.QRect(90, 350, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Current.setFont(font)
        self.Current.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.Current.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Current.setObjectName("Current")
        self.Speed = QtWidgets.QLabel(parent=self.centralwidget)
        self.Speed.setGeometry(QtCore.QRect(140, 390, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Speed.setFont(font)
        self.Speed.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.Speed.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Speed.setObjectName("Speed")
        self.connectivity_indicator = QtWidgets.QLabel(parent=self.centralwidget)
        self.connectivity_indicator.setGeometry(QtCore.QRect(20, 400, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(True)
        self.connectivity_indicator.setFont(font)
        self.connectivity_indicator.setStyleSheet("border-radius: 10px;\n"
"background-color: rgb(255, 0, 0);")
        self.connectivity_indicator.setText("")
        self.connectivity_indicator.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.connectivity_indicator.setObjectName("connectivity_indicator")
        self.Distance_Edit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.Distance_Edit.setGeometry(QtCore.QRect(370, 220, 91, 31))
        font = QtGui.QFont()
        font.setBold(True)
        self.Distance_Edit.setFont(font)
        self.Distance_Edit.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.Distance_Edit.setText("")
        self.Distance_Edit.setObjectName("Distance_Edit")
        self.LowSpeed_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.LowSpeed_Button.setGeometry(QtCore.QRect(470, 220, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        self.LowSpeed_Button.setFont(font)
        self.LowSpeed_Button.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"")
        self.LowSpeed_Button.setObjectName("LowSpeed_Button")
        self.MediumSpeed_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.MediumSpeed_Button.setGeometry(QtCore.QRect(520, 220, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        self.MediumSpeed_Button.setFont(font)
        self.MediumSpeed_Button.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.MediumSpeed_Button.setObjectName("MediumSpeed_Button")
        self.HighSpeed_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.HighSpeed_Button.setGeometry(QtCore.QRect(570, 220, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        self.HighSpeed_Button.setFont(font)
        self.HighSpeed_Button.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.HighSpeed_Button.setObjectName("HighSpeed_Button")
        self.Direction = QtWidgets.QLabel(parent=self.centralwidget)
        self.Direction.setGeometry(QtCore.QRect(60, 390, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Direction.setFont(font)
        self.Direction.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.Direction.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Direction.setObjectName("Direction")
        self.Forwrd_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Forwrd_Button.setGeometry(QtCore.QRect(480, 330, 35, 31))
        self.Forwrd_Button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Forwrd_Button.setAutoFillBackground(False)
        self.Forwrd_Button.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"border-radius: 10px;\n"
"border: 2px solid black;\n"
"")
        self.Forwrd_Button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("forward.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Forwrd_Button.setIcon(icon)
        self.Forwrd_Button.setObjectName("Forwrd_Button")
        self.Right_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Right_Button.setGeometry(QtCore.QRect(520, 360, 35, 31))
        self.Right_Button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Right_Button.setAutoFillBackground(False)
        self.Right_Button.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"border: 2px solid black;\n"
"border-radius: 10px;")
        self.Right_Button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("right.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Right_Button.setIcon(icon1)
        self.Right_Button.setObjectName("Right_Button")
        self.Left_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Left_Button.setGeometry(QtCore.QRect(440, 360, 35, 31))
        self.Left_Button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Left_Button.setAutoFillBackground(False)
        self.Left_Button.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"border: 2px solid black;\n"
"border-radius: 10px;\n"
"\n"
"")
        self.Left_Button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("left.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Left_Button.setIcon(icon2)
        self.Left_Button.setObjectName("Left_Button")
        self.Backward_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Backward_Button.setGeometry(QtCore.QRect(480, 390, 35, 31))
        self.Backward_Button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Backward_Button.setAutoFillBackground(False)
        self.Backward_Button.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"border: 2px solid black;\n"
"border-radius: 10px;")
        self.Backward_Button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("backward.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Backward_Button.setIcon(icon3)
        self.Backward_Button.setObjectName("Backward_Button")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Manual_Button.setText(_translate("MainWindow", "Manual Mode"))
        self.Autonomous_Button.setText(_translate("MainWindow", "Autonomous Mode"))
        self.ScreenShot.setText(_translate("MainWindow", "ScreenShot"))
        self.CV_task1.setText(_translate("MainWindow", "CV Task 1"))
        self.CV_task2.setText(_translate("MainWindow", "CV Task 2"))
        self.Sonar.setText(_translate("MainWindow", "Sonar"))
        self.Voltage.setText(_translate("MainWindow", "Voltage"))
        self.Current.setText(_translate("MainWindow", "Current"))
        self.Speed.setText(_translate("MainWindow", "Speed"))
        self.Distance_Edit.setPlaceholderText(_translate("MainWindow", "Enter Distance"))
        self.LowSpeed_Button.setText(_translate("MainWindow", "Low"))
        self.MediumSpeed_Button.setText(_translate("MainWindow", "Medium"))
        self.HighSpeed_Button.setText(_translate("MainWindow", "High"))
        self.Direction.setText(_translate("MainWindow", "Direction"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
