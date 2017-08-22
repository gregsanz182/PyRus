from FileAudio import FileAudio
from CustomProcess import CustomProcess

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

    def prepareProcess(self) -> CustomProcess:
        process = CustomProcess()
        process.setProgram("resources\\tools\\flac")
        process.extendArg(["--decode", "-c", self.metadata["<path>"]])
        return process
