from FileAudio import *

class FileAAC (AudioFile):

    def __init__(self):
        super().__init__()

    @classmethod
    def isFormatSupported(cls, metaInfo):
        pass
        