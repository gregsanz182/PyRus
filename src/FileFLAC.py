import re
from FileAudio import FileAudio
from CustomProcess import CustomProcess
from PySide.QtCore import QProcess
from Tools import CustomProcess

class FileFLAC (FileAudio):
    """Represents FLAC Audio Files. Contains methods that handles this format.
    This class inherits from FileAudio"""

    def __init__(self, metaInfo: list):
        """Constructor of the class. Initializes and sets all the components."""
        super().__init__(metaInfo)

    @classmethod
    def isFormatSupported(cls, metaInfo: list) -> bool:
        """Returns whether the format of this file is suported."""
        if metaInfo["General"]["Format"].lower() in ("flac", "ogg"):
            if "Audio" in metaInfo:
                if metaInfo["Audio"]["Format"].lower() == "flac":
                    return True

        return False

    def prepareProcess(self) -> CustomProcess:
        """Returns the CustomProcess with commandline arguments defined"""
        process = CustomProcess()
        process.setProgram("resources\\tools\\flac")
        process.extendArg(["--decode", "-c", self.metadata["<path>"]])
        return process

    def analyseProgressLine(self, line: str) -> int:
        """Interprets the line ripped from the CLI"""
        okline = re.search(r"(?P<value>[0-9]*)% complete", line)
        if okline:
            return int(okline.group("value"))
        else:
            return None
