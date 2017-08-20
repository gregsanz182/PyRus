import abc
from PySide.QtGui import QHBoxLayout, QWidget
from FileAudio import FileAudio

class EncoderTools(metaclass=abc.ABCMeta):

    def __init__(self):
        self.preferencesWidget = QWidget()
        self.tagsMapping = {}
        self.defineItems()
        self.defineTagsMapping()

    @abc.abstractmethod
    def defineItems(self):
        pass

    @abc.abstractmethod
    def defineTagsMapping(self):
        pass

    @abc.abstractmethod
    def prepareCMDLine(self, audioFile: FileAudio):
        pass