import threading
import time
import os
from ConversionDialog import ConversionDialog
from TaskThread import TaskThread
from Tools import Tools

class ConversionThread(threading.Thread):

    def __init__(self, listFiles, tool, output=tuple(["", ""])):
        super().__init__()
        self.listFiles = listFiles
        self.backupList = listFiles[:]
        self.tool = tool
        self.output = output
        self.threadsList = []
        self.threadsNum = 2
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
        audioFile = self.listFiles.pop()
        filePath = self.prepareFilePath(audioFile)
        threadAux = TaskThread(self.currentThreadNum, audioFile, self.tool, filePath)
        self.currentThreadNum += 1
        self.threadsList.append(threadAux)
        self.w.connectTask(threadAux.signal, os.path.basename(filePath))
        threadAux.start()

    def prepareFilePath(self, audioFile) -> str:
        filePath = self.output[0]
        if Tools.isAbsolute(os.path.normpath(filePath)) is False:
            filePath = os.path.dirname(audioFile.metadata["<path>"]) + os.sep + filePath

        if self.output[1] == "":
            filePath += os.sep + Tools.getFileNameWithoutExtension(audioFile.metadata["<filename>"])
        else:
            filePath += os.sep + audioFile.getTagsValue(self.output[1])

        filePath += self.tool.getExtension()
        
        filePath = os.path.normpath(filePath)

        Tools.makeFolder(filePath)

        return filePath