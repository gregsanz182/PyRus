import re
from FileAudio import FileAudio
from Tools import CustomProcess

class FileAAC (FileAudio):
    """Represents AAC Audio Files. Contains methods that handles this format.
    This class inherits from FileAudio"""

    def __init__(self, metaInfo: list):
        """Constructor of the class. Initializes and sets all the components."""
        super().__init__(metaInfo)

    @classmethod
    def isFormatSupported(cls, metaInfo: list) -> bool:
        """Returns whether the format of this file is suported."""
        if metaInfo["General"]["Format"].lower() in ("mpeg-4", "adts"):
            if "Audio" in metaInfo:
                if metaInfo["Audio"]["Format"].lower() == "aac":
                    return True

        return False

    def prepareProcess(self) -> CustomProcess:
        """Returns the CustomProcess with commandline arguments defined"""
        process = CustomProcess()
        process.setProgram("resources\\tools\\faad")
        process.extendArg(["-w", self.metadata["<path>"]])
        return process

    def analyseProgressLine(self, line: str) -> int:
        """Interprets the line ripped from the CLI"""
        okline = re.search(r"\[(?P<current>[0-9]*)%\] decoding", line)
        if okline:
            return int(okline.group("current"))
        else:
            return None
