from FileAudio import FileAudio

class FileAAC (FileAudio):
    """Represents AAC Audio Files. Contains methods that handles this format.
    This class inherits from FileAudio"""

    def __init__(self, metaInfo):
        """Constructor of the class. Initializes and sets all the components."""
        super().__init__(metaInfo)

    @classmethod
    def isFormatSupported(cls, metaInfo):
        """Returns whether the format of this file is suported."""
        if metaInfo["General"]["Format"].lower() in ("mpeg-4", "adts"):
            if "Audio" in metaInfo:
                if metaInfo["Audio"]["Format"].lower() == "aac":
                    return True

        return False
        