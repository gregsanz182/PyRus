from FileAudio import FileAudio
from CustomProcess import CustomProcess
from PySide.QtCore import QProcess

class FileFLAC (FileAudio):
    """Represents FLAC Audio Files. Contains methods that handles this format.
    This class inherits from FileAudio"""

    def __init__(self, metaInfo):
        """Constructor of the class. Initializes and sets all the components."""
        super().__init__(metaInfo)

    @classmethod
    def isFormatSupported(cls, metaInfo):
        """Returns whether the format of this file is suported."""
        if metaInfo["General"]["Format"].lower() in ("flac", "ogg"):
            if "Audio" in metaInfo:
                if metaInfo["Audio"]["Format"].lower() == "flac":
                    return True

        return False

    def runProcess(self, signal, encProcess):
        decProcess = CustomProcess()
        decProcess.setProgram("resources\\tools\\flac")
        decProcess.extendArg(["--decode", "-c", self.metadata["<path>"]])

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
