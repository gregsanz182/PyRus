from FileAudio import *

class FileMP3 (FileAudio):

    def __init__(self, metaInfo):
        super().__init__(metaInfo)

    @classmethod
    def isFormatSupported(cls, metaInfo):
        if "Audio" in metaInfo:
            if metaInfo["Audio"]["Format"].lower() == "mpeg audio" \
               and metaInfo["Audio"]["Format version"].lower() in ["version 1", "version 2", "version 3"] \
               and metaInfo["Audio"]["Format profile"].lower() in ["layer 1", "layer 2", "layer 3"]:
                return True

        return False
