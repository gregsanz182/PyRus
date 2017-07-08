import sys
from PySide.QtGui import *
from MainWindow import *

if __name__ == '__main__':
    try:
        mainApp = QApplication(sys.argv)
        
        mainWindow = MainWindow()
        mainWindow.show()

        mainApp.exec_()
        sys.exit(0)
    except NameError:
        print("Name error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing window...")
    except Exception:
        print(sys.exc_info()[1])

