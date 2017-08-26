import abc
from PySide.QtGui import QHBoxLayout, QWidget
from FileAudio import FileAudio
from Tools import CustomProcess

class EncoderTools(metaclass=abc.ABCMeta):
    """Abstract class that provides Encoders Components"""

    def __init__(self):
        """Constructor of the class"""
        self.preferencesWidget = QWidget()
        self.tagsMapping = {}
        self.defineItems()
        self.defineTagsMapping()

    @abc.abstractmethod
    def defineItems(self):
        """Defines the items of the Tool"""
        pass

    @abc.abstractmethod
    def defineTagsMapping(self):
        """Defines the mapping of the tags to the corresponding encoder"""
        pass

    @abc.abstractmethod
    def prepareProcess(self, audioFile: FileAudio, outputPath: str) -> CustomProcess:
        """Returns the CustomProcess with commandline arguments difined"""
        pass

    @abc.abstractmethod
    def getExtension(self) -> str:
        """Returns the extension selected in the Tool"""
        pass