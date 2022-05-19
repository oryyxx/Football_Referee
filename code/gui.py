from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import camera
import score
import time

duration = 0

#Construction for the window application
class Gui(QWidget):
    def __init__(self):
        super(Gui, self).__init__()

        #setting up labels and GUI using Pyqt
        self.setWindowTitle("Football Referee")
        self.VBL = QVBoxLayout()

        self.FeedLabel = QLabel()
        self.ScoreALabel = QLabel(("Team A: " + str(score.getScore('a'))), self)
        self.ScoreBLabel = QLabel(("Team B: " + str(score.getScore('b'))), self)
        self.ProcessDur = QLabel(("Proccess Duration: " + str(round(duration)) + "ms"), self)

        self.VBL.addWidget(self.FeedLabel)
        self.VBL.addWidget(self.ScoreALabel)
        self.VBL.addWidget(self.ScoreBLabel)
        self.VBL.addWidget(self.ProcessDur)
        
        self.ResetButton = QPushButton("Reset")
        self.ResetButton.clicked.connect(score.resetScore)
        self.VBL.addWidget(self.ResetButton)

        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)

    #Calls when its time to update the gui
    def ImageUpdateSlot(self, image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(image))
        self.ScoreALabel.setText(("Team A: " + str(score.getScore('a'))))
        self.ScoreBLabel.setText(("Team B: " + str(score.getScore('b'))))
        self.ProcessDur.setText(("Proccess Duration: " + str(round(duration)) + "ms"))



#Capture video from camera is being dealt from a seperate "thread" than the main thread to prevent freeze.
class Worker1(QThread):
    global duration

    ImageUpdate = pyqtSignal(QImage)

    def run(self):

        self.ThreadActive = True

        # "Main loop" - computer vision should be moved to a different loop
        while self.ThreadActive:
            global duration

            #get the current time in ns to calculate duration for proccessing
            t = time.time_ns() 

            #updating image from webcam
            camera.updateImage()

            #computer vision should be proccessed here (for now)

            #fetching image to display on the gui
            image = camera.getImage()

            #image being converted to QImage for displaying (for Pyqt to render it)
            ConvertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            Pic = ConvertToQtFormat.scaled(1080, 720, Qt.KeepAspectRatio)
            self.ImageUpdate.emit(Pic)

            #get current time and subtract it by t
            duration = time.time_ns() - t

            #convert duration from ns to milisec
            duration = duration / 1000000

    def stop(self):
        self.ThreadActive = False
        self.quit()