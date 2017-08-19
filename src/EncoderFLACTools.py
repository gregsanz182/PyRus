from PySide.QtGui import QLabel
from EncoderTools import EncoderTools
from GuiTools import CustomComboBox, CustomHFormLayout

class EncoderFLACTools(EncoderTools):

    def __init__(self):
        super().__init__()
        self.layout = CustomHFormLayout(self.preferencesWidget)
        self.layout.setContentsMargin(0)

        self.compressionLevelBox = CustomComboBox()
        self.compressionLevelBox.addItems(self.compressionLevelsText)
        self.compressionLevelBox.setCurrentIndex(3)
        self.layout.addField(QLabel("Compression Level"), self.compressionLevelBox)

        self.containerBox = CustomComboBox()
        self.containerBox.addItems(self.containerList)
        self.containerBox.setCurrentIndex(0)
        self.layout.addField(QLabel("Container"), self.containerBox)


    def defineItems(self):
        self.formatName = "FLAC | Free Lossless Audio Codec"
        self.compressionLevels = "8 7 6 5 4 3 2 1 0".split(" ")
        self.compressionLevelsText = []
        for level in self.compressionLevels:
            if level == "8":
                self.compressionLevelsText.append(level+" (Best)")
            elif level == "5":
                self.compressionLevelsText.append(level+" (Default)")
            elif level == "0":
                self.compressionLevelsText.append(level+" (Fast)")
            else:
                self.compressionLevelsText.append(level)
        self.containerList = [".flac", ".ogg"]

    def beginEncoding(self):
        cmdline = "flac"
        if self.containerBox.currentIndex() == 1:
            cmdline += " --ogg"
        cmdline += " -"+self.compressionLevels[self.compressionLevelBox.currentIndex()]

        print(cmdline)
