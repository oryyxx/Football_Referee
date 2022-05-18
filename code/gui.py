from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import camera
import score

#Construction for the window application
class Gui(QWidget):
    def __init__(self):
        super(Gui, self).__init__()

        self.setWindowTitle("Football Referee")
        self.VBL = QVBoxLayout()

        self.FeedLabel = QLabel()
        self.ScoreALabel = QLabel(("Team A: " + str(score.getScore('a'))), self)
        self.ScoreBLabel = QLabel(("Team B: " + str(score.getScore('b'))), self)

        self.VBL.addWidget(self.FeedLabel)
        self.VBL.addWidget(self.ScoreALabel)
        self.VBL.addWidget(self.ScoreBLabel)
        
        self.ResetButton = QPushButton("Reset")
        self.ResetButton.clicked.connect(score.resetScore)
        self.VBL.addWidget(self.ResetButton)

        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)

    def ImageUpdateSlot(self, image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(image))
        self.ScoreALabel.setText(("Team A: " + str(score.getScore('a'))))
        self.ScoreBLabel.setText(("Team B: " + str(score.getScore('b'))))



#Capture video from camera is being dealt from a seperate "thread" than the main thread to prevent freeze.
class Worker1(QThread):

    ImageUpdate = pyqtSignal(QImage)

    def run(self):

        self.ThreadActive = True
        while self.ThreadActive:

            camera.updateImage()
            image = camera.getImage()

            ConvertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            Pic = ConvertToQtFormat.scaled(1080, 720, Qt.KeepAspectRatio)
            self.ImageUpdate.emit(Pic)

    def stop(self):
        self.ThreadActive = False
        self.quit()


