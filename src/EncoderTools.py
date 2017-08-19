from PySide.QtGui import QHBoxLayout, QWidget
import abc

class EncoderTools(metaclass=abc.ABCMeta):

    def __init__(self):
        self.preferencesWidget = QWidget()
        self.defineItems()

    @abc.abstractmethod
    def defineItems(self):
        pass

    @abc.abstractmethod
    def beginEncoding(self, fileList: list):
        pass