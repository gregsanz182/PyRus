import re
from FileAudio import FileAudio
from CustomProcess import CustomProcess

class FileMP3 (FileAudio):
    """Represents MP3 Audio Files. Contains methods that handles this format.
    This class inherits from FileAudio"""

    def __init__(self, metaInfo):
        """Constructor of the class. Initializes and sets all the components."""
        super().__init__(metaInfo)

    @classmethod
    def isFormatSupported(cls, metaInfo):
        """Returns whether the format of this file is suported."""
        if "Audio" in metaInfo:
            if metaInfo["Audio"]["Format"].lower() == "mpeg audio" \
               and metaInfo["Audio"]["Format version"].lower() in ["version 1", "version 2", "version 3"] \
               and metaInfo["Audio"]["Format profile"].lower() in ["layer 1", "layer 2", "layer 3"]:
                return True

        return False
    
    def prepareProcess(self) -> CustomProcess:
        process = CustomProcess()
        process.setProgram("resources\\tools\\lame")
        process.extendArg(["--decode", "--verbose", self.metadata["<path>"], "-"])
        return process

    def analyseProgressLine(self, line: str):
        okline = re.search(r"Frame# *(?P<current>[0-9]*)/(?P<total>[0-9]*)", line)
        if okline:
            return int((int(okline.group("current"))/int(okline.group("total")))*100)
        else:
            return None
