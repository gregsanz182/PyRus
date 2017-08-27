import os
from copy import deepcopy
from PySide.QtCore import QProcess

class OSTools():

    def __init__(self):
        pass

    @classmethod
    def isAbsolute(self, normPath: str) -> bool:
        parts = normPath.split(os.sep)
        try:
            if os.path.ismount(parts[0]+os.sep):
                return True
        except FileNotFoundError:
            return False
        return False

    @classmethod
    def getFileNameWithoutExtension(self, filename: str) -> str:
        pointIndex = filename.rfind(".")
        if pointIndex != -1:
            return filename[:pointIndex]
        return filename

    @classmethod
    def makeFolder(self, path: str):
        dirName = os.path.dirname(path)
        if os.path.exists(dirName) is False:
            os.makedirs(dirName)

class ProgressObject():

    Task_Prepared = 0
    Task_Converting = 1
    Task_Cancelled = 2

    def __init__(self):
        self.actualProgress = 0
        self.incrementedProgress = 0
        self.state = self.Task_Prepared

    def updateProgress(self, progress: int):
        diff = self.incrementedProgress = progress - self.actualProgress
        if diff > 0:
            self.actualProgress = progress
            self.incrementedProgress = diff

    def updateState(self, state: int):
        self.state = state

    def getProgress(self):
        return deepcopy(self)

class CustomProcess(QProcess):

    def __init__(self):
        super().__init__()
        self.args = []
        self.program = ""

    def startProcess(self):
        self.start(self.program, self.args)

    def setProgram(self, program: str):
        self.program = program

    def appendArg(self, arg: str):
        self.args.append(arg)

    def extendArg(self, argsList: list):
        self.args.extend(argsList)
        
    def printArgs(self):
        for arg in self.args:
            print(arg, end=" ")
