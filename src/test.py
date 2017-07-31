from PySide.QtCore import *
from PySide.QtGui import *
import base64
import sys
import hashlib
import subprocess

class MyModel():

    def __init__(self):
        super().__init__()
        self.faad = QProcess()
        self.lame = QProcess()
        self.faad.setStandardOutputProcess(self.lame)
        self.faad.setProcessChannelMode(QProcess.MergedChannels)
        self.faad.setReadChannel(QProcess.StandardOutput)
        self.faad.start("lame", ["--decode", "sss.mp3", "hola.wav"])
        self.lame.start("lame", ["-b 128", "-", "haha.mp3"])

        while True:
            self.faad.waitForReadyRead()
            if self.faad.bytesAvailable() > 0:
                print(self.faad.readLine())

        self.faad.waitForFinished(-1)
        self.lame.waitForFinished(-1)

    def leer(self):
        print("aqui")
        while self.faad.bytesAvailable() > 0:
            try:
                print(self.faad.readLine())
            except Exception:
                print("Error")

if __name__ == "__main__":
    """faad = QProcess()
    lame = QProcess()

    faad.setStandardOutputProcess(lame)
    lame.setReadChannel(lame.StandardOutput)

    faad.start("faad", ["-w", "sss.m4a"])
    lame.start("lame", ["-b 128", "-", "hola123.mp3"])

    while True:
        print(lame.readAllStandardError())

    lame.waitForFinished()
    faad.waitForFinished()

    lame.close()"""

    h = MyModel()

    """h = subprocess.Popen("mpg123 -v -w holaa.wav hola123.mp3", shell=True)

    h.wait()

    print(h.returncode)"""

    
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


