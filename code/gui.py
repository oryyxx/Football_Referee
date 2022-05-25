from tkinter import Menubutton
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMenu
from matplotlib.pyplot import show
import camera
import score
import time
import tracker
import draw

#temp variables
duration = 0
fps = 0
showFPS = False
isGameRunning = False

#Construction for the window application
class Gui(QMainWindow):
    def __init__(self):
        super(Gui, self).__init__()

        self._createMenuBarActions()
        self._createMenuBar()
        self._connectAction()

        #setting up labels and GUI using Pyqt
        self.setWindowTitle("Football Referee")
        self.centralWidget = QLabel()
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)

        #self.VBL = QVBoxLayout()

        #self.FeedLabel = QLabel()
        #self.ScoreALabel = QLabel(("Team A: " + str(score.getScore('a'))), self)
        #self.ScoreBLabel = QLabel(("Team B: " + str(score.getScore('b'))), self)

        #self.VBL.addWidget(self.FeedLabel)
        #self.VBL.addWidget(self.ScoreALabel)
        #self.VBL.addWidget(self.ScoreBLabel)
        
        #self.ResetButton = QPushButton("Reset")
        #self.ResetButton.clicked.connect(score.resetScore)
        #self.VBL.addWidget(self.ResetButton)

        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.UpdateFeed)
        

    def _createMenuBar(self):
        menuBar = self.menuBar()

        gameMenu = QMenu("&Game", self)
        debugMenu = QMenu("&Debug", self)

        menuBar.addMenu(gameMenu)
        menuBar.addMenu(debugMenu)

        debugMenu.addAction(self.fpsAction)

        gameMenu.addAction(self.gameStart)
        gameMenu.addAction(self.gameReset)
        gameMenu.addAction(self.gamePause)
        gameMenu.addAction(self.gameExit)
        
    
    def _createMenuBarActions(self):

        self.fpsAction = QAction("&FPS...", self)
        
        self.gameStart = QAction("&Start", self)
        self.gamePause = QAction("&Pause", self)
        self.gameReset = QAction("&Restart",self)
        self.gameExit = QAction("&Exit",self)

    def _connectAction(self):

        self.fpsAction.triggered.connect(self.fpsActionTriggered)

        self.gameStart.triggered.connect(self.gameStartTrig)
        self.gamePause.triggered.connect(self.gamePauseTrig)
        self.gameReset.triggered.connect(self.gameResetTrig)
        self.gameExit.triggered.connect(self.gameExitTrig)

    #------------------ Menu Actions ------------------
    def fpsActionTriggered(self):
        global showFPS

        if showFPS:
            showFPS = False
        else:
            showFPS = True
    
    def gameStartTrig(self):
        global isGameRunning

        if not isGameRunning:
            isGameRunning = True
        
        self.gameResetTrig()

        print("start pressed")
    
    def gameResetTrig(self):
        
        score.resetScore()
        print("restart pressed")
    
    def gamePauseTrig(self):
        print("Pause pressed")

    def gameExitTrig(self):
        print("start pressed")
    
    #Calls when its time to update the gui
    def UpdateFeed(self, image):
        self.centralWidget.setPixmap(QPixmap.fromImage(image))



#Capture video from camera is being dealt from a seperate "thread" than the main thread to prevent freeze.
class Worker1(QThread):
    global duration

    ImageUpdate = pyqtSignal(QImage)

    def run(self):

        self.ThreadActive = True

        # "Main loop" - computer vision should be moved to a different loop
        while self.ThreadActive:
            global duration
            global fps

            #get the current time in ns to calculate duration for proccessing
            t = time.time_ns() 

            #updating image from webcam
            camera.updateImage()

            #fetching the latest image
            image = camera.getImage()

            #---------- computer vision should be proccessed here (for now) ------  

            #finalImage = tracker.trackHand(image)
            #image = draw.rect(image, "rect", 100, 100, 200, 200, 3)


            # ----------------------------------------------------------------------

            #draw fps on image
            if(showFPS):
                image = draw.fps(image, round(fps))

            #draw score on image
            image = draw.score(image, score.getScore('a'), score.getScore('b'))

            #image being converted to QImage for displaying (for Pyqt to render it)
            ConvertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            Pic = ConvertToQtFormat.scaled(1080, 720, Qt.KeepAspectRatio)
            self.ImageUpdate.emit(Pic)

            #get current time and subtract it by t
            duration = time.time_ns() - t

            #convert duration from ns to milisec
            duration = duration / 1000000

            fps = 1000 / duration

    def stop(self):
        self.ThreadActive = False
        camera.closeCamera()
        self.quit() 