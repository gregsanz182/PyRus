from PySide.QtGui import QHBoxLayout
from PySide.QtCore import Qt
from EncoderTools import EncoderTools
from GuiTools import ComboBox

class EncoderFLACTools(EncoderTools):

    def __init__(self):
        super().__init__()
        self.defineItems()
        self.layout = QHBoxLayout(self.preferencesWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.containerBox = ComboBox()
        self.containerBox.addItems(self.containerList)
        self.containerBox.setCurrentIndex(0)


        self.compressionLevelBox = ComboBox()
        self.compressionLevelBox.addItems(self.compressionLevels)
        self.compressionLevelBox.setCurrentIndex(3)

        self.layout.addWidget(self.containerBox)
        self.layout.addWidget(self.compressionLevelBox)

        self.layout.addStretch()

    def defineItems(self):
        self.formatName = "FLAC | Free Lossless Audio Codec"
        self.compressionLevels = ["8 (Best)", "7", "6", "5 (Default)", "4", "3", "2", "1", "0 (Fast)"]
        self.containerList = [".flac", ".ogg"]
