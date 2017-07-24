from FileAudio import *

class FileAAC (FileAudio):

    def __init__(self, metaInfo):
        super().__init__(metaInfo)

    @classmethod
    def isFormatSupported(cls, metaInfo):
        if metaInfo["General"]["Format"].lower() in ("mpeg-4", "adts"):
            if "Audio" in metaInfo:
                if metaInfo["Audio"]["Format"].lower() == "aac":
                    return True

        return False
        