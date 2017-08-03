from PySide.QtGui import QLabel
from EncoderTools import EncoderTools
from GuiTools import CustomComboBox, CustomHFormLayout

class EncoderFLACTools(EncoderTools):

    def __init__(self):
        super().__init__()
        self.defineItems()
        self.layout = CustomHFormLayout(self.preferencesWidget)
        self.layout.setContentsMargin(0)

        self.compressionLevelBox = CustomComboBox()
        self.compressionLevelBox.addItems(self.compressionLevels)
        self.compressionLevelBox.setCurrentIndex(3)
        self.layout.addField(QLabel("Compression Level"), self.compressionLevelBox)

        self.containerBox = CustomComboBox()
        self.containerBox.addItems(self.containerList)
        self.containerBox.setCurrentIndex(0)
        self.layout.addField(QLabel("Container"), self.containerBox)


    def defineItems(self):
        self.formatName = "FLAC | Free Lossless Audio Codec"
        self.compressionLevels = ["8 (Best)", "7", "6", "5 (Default)", "4", "3", "2", "1", "0 (Fast)"]
        self.containerList = [".flac", ".ogg"]
