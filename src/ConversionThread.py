import threading
import time
import os
from ConversionDialog import ConversionDialog
from TaskThread import TaskThread
from Tools import OSTools
from EncoderTools import EncoderTools
from FileAudio import FileAudio

class ConversionThread(threading.Thread):
    """The thread than handles all the other conversion threads and controls
    the conversion gloab task"""

    def __init__(self, listFiles: list, tool: EncoderTools, output: tuple=tuple(["", ""])):
        """Constructor of the class. The argument 'listFiles' is the list of files to convert.
        'tool' corresponds to the encoder tool that contains the encoder methods.
        'output' contains the output preferences as a tuple"""
        super().__init__()
        self.listFiles = listFiles
        self.backupList = listFiles[:]
        self.tool = tool
        self.output = output

        #List of active threads
        self.threadsList = []

        #Number of parallel threads that the user wants
        self.threadsNum = 1

        #State of the global thread
        self.state = 0

        #This serves as a counter of files converted and as a thread ID
        self.currentThreadNum = 0

        #Conversion dialog that shows the progress of the conversion
        self.conversionDialog = ConversionDialog()
        self.conversionDialog.setTotalProgressBarMaximum(len(self.listFiles)*100)
        self.makeConnections()

    def run(self):
        """Thread activity. Is here where the thread do its task"""
        while self.state == 1:
            if len(self.threadsList) < self.threadsNum and self.currentThreadNum < len(self.listFiles):
                self.addAndStartTask()

            for thr in self.threadsList[:]:
                if thr.isAlive() is False:
                    self.threadsList.remove(thr)

            idleBars = self.conversionDialog.visibleBars() - self.threadsNum
            if idleBars > 0:
                self.conversionDialog.hideIdleBars(idleBars)

            if len(self.threadsList) <= 0 and self.currentThreadNum >= len(self.listFiles):
                self.state = 2
            time.sleep(0.1)
        

    def beginThread(self):
        """Sets the state of the conversion thread to 1 and starts it.
        This method also executes the Converion Dialog"""
        self.state = 1
        self.start()
        self.conversionDialog.exec_()

    def makeConnections(self):
        """Makes the connections between the items"""
        self.conversionDialog.numThreadsWidget.counterChanged.connect(self.changeNumberThreads)

    def changeNumberThreads(self, num: int):
        """This slot change the number of threads that the user requires."""
        self.threadsNum = num

    def addAndStartTask(self):
        """Adds a thread to the list of threads and starts it.
        Also makes the connection to the corresponding bar of the thread"""
        audioFile = self.listFiles[self.currentThreadNum]
        filePath = self.prepareFilePath(audioFile)
        threadAux = TaskThread(self.currentThreadNum, audioFile, self.tool, filePath)
        self.threadsList.append(threadAux)
        self.conversionDialog.connectTask(threadAux.updateSignal, audioFile.metadata["<path>"])
        threadAux.start()
        self.currentThreadNum += 1

    def prepareFilePath(self, audioFile: FileAudio) -> str:
        """Prepare the output file path of the file passed as argument"""
        filePath = self.output[0]

        if OSTools.isAbsolute(os.path.normpath(filePath)) is False:
            filePath = os.path.dirname(audioFile.metadata["<path>"]) + os.sep + filePath
        if self.output[1] == "":
            filePath += os.sep + OSTools.getFileNameWithoutExtension(audioFile.metadata["<filename>"])
        else:
            filePath += os.sep + audioFile.getTagsValue(self.output[1])
        
        filePath += self.tool.getExtension()
        filePath = os.path.normpath(filePath)
        OSTools.makeFolder(filePath)
        return filePath