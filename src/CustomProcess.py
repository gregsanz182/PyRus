from PySide.QtCore import QProcess

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
