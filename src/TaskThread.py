import threading
import os
from PySide.QtCore import QProcess, Signal, QObject
from EncoderTools import EncoderTools
from CustomProcess import CustomProcess
from Tools import ProgressObject

class TaskThread(QObject, threading.Thread):

    updateSignal = Signal(ProgressObject, str)

    def __init__(self, threadNumber, audioFile, tool, outputPath):
        QObject.__init__(self)
        threading.Thread.__init__(self)
        self.threadNumber = threadNumber
        self.audioFile = audioFile
        self.tool = tool
        self.outputPath = outputPath
        self.progress = ProgressObject()

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
                for line in str(decProcess.readLine()).replace("\b", "\n").splitlines():
                    progValue = self.audioFile.analyseProgressLine(line)
                    if progValue:
                        self.progress.updateProgress(progValue)
                        self.updateSignal.emit(self.progress, self.threadNumber)

        decProcess.waitForFinished(-1)
        encProcess.waitForFinished(-1)

        self.progress.updateProgress(100)
        self.progress.updateState(ProgressObject.Task_Converting)
        self.updateSignal.emit(self.progress, self.threadNumber)
