import threading
import os
from PySide.QtCore import QProcess
from EncoderTools import EncoderTools
from CustomProcess import CustomProcess
from Tools import Tools

class TaskThread(threading.Thread):

    dirLock = threading.Lock()

    def __init__(self, threadNumber, audioFile, tool, outputPath):
        super().__init__()
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
