import gui
import sys

def init():
    app = gui.QApplication(sys.argv)
    root = gui.Gui()
    root.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    init()
    