import threading
import os
from PySide.QtCore import QProcess, Signal, QObject
from EncoderTools import EncoderTools
from CustomProcess import CustomProcess
from Tools import Tools

class TaskThread(QObject, threading.Thread):

    updateSignal = Signal(int, int, str)
    
    def __init__(self, threadNumber, audioFile, tool, outputPath):
        QObject.__init__(self)
        threading.Thread.__init__(self)
        self.threadNumber = threadNumber
        self.audioFile = audioFile
        self.tool = tool
        self.outputPath = outputPath

    def run(self):
        self.audioFile.startDecoding(self.updateSignal, self.tool.prepareProcess(self.audioFile, self.outputPath))
