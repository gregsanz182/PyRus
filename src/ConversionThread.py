import threading
import time
import os
from ConversionDialog import ConversionDialog
from TaskThread import TaskThread

class ConversionThread(threading.Thread):

    def __init__(self, listFiles, tool, output=tuple(None, None)):
        super().__init__()
        self.listFiles = listFiles
        self.backupList = listFiles[:]
        self.tool = tool
        self.output = output
        self.threadsList = []
        self.threadsNum = 1
        self.state = 0
        self.currentThreadNum = 0
        self.w = ConversionDialog()
        self.makeConnections()

    def run(self):
        while self.state == 1:
            if len(self.threadsList) < self.threadsNum and len(self.listFiles) > 0:
                self.addAndStartTask()

            for thr in self.threadsList[:]:
                if thr.isAlive() is False:
                    self.threadsList.remove(thr)

            if len(self.threadsList) <= 0 and len(self.listFiles) <= 0:
                self.state = 2
            time.sleep(0.1)
        

    def beginThread(self):
        self.state = 1
        self.start()
        self.w.exec_()

    def makeConnections(self):
        self.w.numThreadsWidget.counterChanged.connect(self.changeNumberThreads)

    def changeNumberThreads(self, num: int):
        self.threadsNum = num

    def addAndStartTask(self):
        threadAux = TaskThread(self.currentThreadNum, self.listFiles.pop(), self.tool, self.output)
        self.currentThreadNum += 1
        self.threadsList.append(threadAux)
        threadAux.start()
