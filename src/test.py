from PySide.QtCore import QProcess
from PySide.QtGui import *
import base64
import sys
import hashlib
import subprocess
import _thread
import time
import re

class MyModel():

    def __init__(self):
        super().__init__()
        self.faad = QProcess()
        self.lame = QProcess()
        self.faad.setStandardOutputProcess(self.lame)
        self.faad.setReadChannel(QProcess.StandardError)
        self.faad.start("resources\\tools\\flac", ["--decode", "-c", "C:\\Users\\fmlia\\Desktop\\06- Cassandra asdasd.flac"])
        self.lame.start("resources\\tools\\flac", ["-5", "--totally-silent", '--output-name=hah 2a.flac', "-"])

        while self.faad.state() != QProcess.NotRunning:
            self.faad.waitForReadyRead()
            while self.faad.bytesAvailable() > 0:
                print(str(self.faad.readLine()).replace("\b", ""))

        self.faad.waitForFinished(-1)
        self.lame.waitForFinished(-1)

        print(self.faad.exitCode())

    def leer(self):
        print("aqui")
        while self.faad.bytesAvailable() > 0:
            try:
                print(self.faad.readLine())
            except Exception:
                print("Error")

class CustomBufferStream():

    def __init__(self, stdout):
        pass


if __name__ == "__main__":

    #regxp = re.compile("[0-9]* complete")


    """def print_time(threadName, delay):
        count = 0
        while count < 5:
            time.sleep(delay)
            count += 1
            print("%s: %s" % (threadName, time.ctime(time.time())))

    try:
        _thread.start_new_thread(print_time, ("Thread-1", 2, ))
        _thread.start_new_thread(print_time, ("Thread-2", 4, ))
    except:
        print("Error: unable to start thread")

    while 1:
        pass"""
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

    """h = subprocess.Popen('flac --decode -c "E:\\Descargas\\Steven Wilson - Hand. Cannot. Erase. (2015) [FLAC]\\Disc 1of2\\01 - First Regret.flac" | lame --quiet - test2.mp3', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    while True:
        output = h.stdout.read(50)
        if len(output) <= 0 and h.poll() is not None:
            break
        print(output)"""

    """h = subprocess.Popen(['flac', '--decode', '-c', 'C:\\Users\\fmlia\\Desktop\\06- Cassandra Gemini.flac'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    h2 = subprocess.Popen(['lame', '--quiet', '-', 'test2.mp3'], stdin=h.stdout)
    h.stdout.close()
    for i in range(6):
        output = h.stderr.readline()
    output = h.stderr.read(27)
    print(output)
    while True:
        output = h.stderr.read1(-1)
        if len(output) <= 0 and h.poll() is not None:
            break
        print(output)"""


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


