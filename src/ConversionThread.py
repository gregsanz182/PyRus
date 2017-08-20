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
        self.w = ConversionDialog()
        self.makeConnections()

    def run(self):
        flag = True
        while self.state == 1:
            if len(self.threadsList) < self.threadsNum:
                self.addThread()

            for thr in self.threadsList:
                if thr.isAlive() is False:
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

    def addThread(self):
        threadAux = TaskThread(self.currentThreadNum, self.listFiles[0], self.tool)
        self.currentThreadNum += 1
        self.threadsList.append(threadAux)
        threadAux.start()
