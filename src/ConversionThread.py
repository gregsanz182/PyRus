import threading
import time
from ConversionDialog import ConversionDialog
from TaskThread import TaskThread

class ConversionThread(threading.Thread):

    def __init__(self, listFiles, tool, output=None, outputTemplate=None):
        super().__init__()
        self.listFiles = listFiles
        self.returnList = listFiles[:]
        self.tool = tool
        self.output = output
        self.outputTemplate = outputTemplate
        self.threadsList = []
        self.threadsNum = 1
        self.state = 0
        self.currentThreadNum = 0

    def run(self):
        while self.state == 1:
            if len(self.threadsList) < self.threadsNum:
                self.addThread()
        

    def beginThread(self):
        self.w = ConversionDialog()
        self.state = 1
        #self.start()
        self.w.exec_()

    def numberThreadsChanged(self, num):
        self.threadsNum = int(num)

    def addThread(self):
        threadAux = TaskThread(self.currentThreadNum)
        self.currentThreadNum += 1
        self.threadsList.append(threadAux)
        threadAux.start()
