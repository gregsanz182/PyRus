from PySide.QtCore import *
from PySide.QtGui import *
import base64
import sys
import hashlib

class MyModel(QWidget):

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(1280)
        self.setMinimumHeight(720)
        self.pix = QPixmap("nocover.png")
        self.label = QLabel()
        self.label.setPixmap(self.pix.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.este = QVBoxLayout()
        self.setLayout(self.este)
        self.este.addWidget(self.label)
        self.este.addStretch()

if __name__ == "__main__":
    hash_md5 = hashlib.md5()
    with open("nocover.png", "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    print(hash_md5.hexdigest())
    """try:
        mainApp = QApplication(sys.argv)

        mainWindow = MyModel()
        mainWindow.show()

        mainApp.exec_()
        sys.exit(0)
    except NameError:
        print("Name error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing window...")
    except Exception:
        print(sys.exc_info()[1])"""


