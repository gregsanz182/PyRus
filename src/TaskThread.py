import threading
import os
from PySide.QtCore import QProcess
from EncoderTools import EncoderTools
from CustomProcess import CustomProcess
from Tools import Tools

class TaskThread(threading.Thread):

    dirLock = threading.Lock()

    def __init__(self, threadNumber, audioFile, tool, output):
        super().__init__()
        self.threadNumber = threadNumber
        self.audioFile = audioFile
        self.tool = tool
        self.output = output

    def run(self):
        decProcess = self.audioFile.prepareProcess()
        encProcess = self.tool.prepareProcess(self.audioFile, self.prepareFilePath())

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

    def prepareFilePath(self) -> str:
        filePath = self.output[0]
        if Tools.isAbsolute(os.path.normpath(filePath)) is False:
            filePath = os.path.dirname(self.audioFile.metadata["<path>"]) + os.sep + filePath

        if self.output[1] == "":
            filePath += os.sep + Tools.getFileNameWithoutExtension(self.audioFile.metadata["<filename>"])
        else:
            filePath += os.sep + self.audioFile.getTagsValue(self.output[1])

        filePath += self.tool.getExtension()
        
        filePath = os.path.normpath(filePath)

        return filePath
