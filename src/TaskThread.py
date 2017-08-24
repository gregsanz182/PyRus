import threading
import os
from PySide.QtCore import QProcess, Signal, QObject
from EncoderTools import EncoderTools
from CustomProcess import CustomProcess
from Tools import Tools

class TaskThread(QObject, threading.Thread):

    dirLock = threading.Lock()
    signal = Signal(int, int, str)

    def __init__(self, threadNumber, audioFile, tool, outputPath):
        QObject.__init__(self)
        threading.Thread.__init__(self)
        self.threadNumber = threadNumber
        self.audioFile = audioFile
        self.tool = tool
        self.outputPath = outputPath

    def run(self):
        decProcess = self.audioFile.prepareProcess()
        encProcess = self.tool.prepareProcess(self.audioFile, self.outputPath)

        decProcess.setStandardOutputProcess(encProcess)
        decProcess.setReadChannel(QProcess.StandardError)

        decProcess.startProcess()
        encProcess.startProcess()

        while decProcess.state() != QProcess.NotRunning:
            decProcess.waitForReadyRead()
            while decProcess.bytesAvailable() > 0:
                print(str(decProcess.readLine()).replace("\b", ""))

        decProcess.waitForFinished(-1)
        encProcess.waitForFinished(-1)

        self.signal.emit(100, self.threadNumber, "Completed")
