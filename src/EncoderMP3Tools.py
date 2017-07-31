from PySide.QtGui import QHBoxLayout, QComboBox, QStackedWidget, QWidget
from PySide.QtCore import QSize
from EncoderTools import EncoderTools
from GuiTools import HWidget

class EncoderMP3Tools(EncoderTools):

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self.preferencesWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.defineItems()

        self.bitrateModeBox = QComboBox()
        self.bitrateModeBox.addItems(self.listBitrateModes)
        self.layout.addWidget(self.bitrateModeBox)

        self.stackedWidget = QStackedWidget()
        self.layout.addWidget(self.stackedWidget)

        """self.CBRWidget = HWidget()
        self.bitrateCBRMode = QComboBox()
        self.bitrateCBRMode.addItems(self.listBitrates)
        self.CBRWidget.addWidget(self.bitrateCBRMode)
        self.channelCBRMode = QComboBox()
        self.channelCBRMode.addItems(self.listChannels)
        self.CBRWidget.addWidget(self.channelCBRMode)
        self.CBRWidget.addStretch()
        self.stackedWidget.addWidget(self.CBRWidget)

        self.VBRWidget = HWidget()
        self.qualityVBRMode = QComboBox()
        self.qualityVBRMode.addItems(self.listQualityLevels)
        self.VBRWidget.addWidget(self.qualityVBRMode)
        self.channelVBRMode = QComboBox()
        self.channelVBRMode.addItems(self.listChannels)
        self.VBRWidget.addWidget(self.channelVBRMode)
        self.VBRWidget.addStretch()
        self.stackedWidget.addWidget(self.VBRWidget)

        self.ABRWidget = HWidget()
        self.bitrateABRMode = QComboBox()
        self.bitrateABRMode.addItems(self.listBitrates)
        self.ABRWidget.addWidget(self.bitrateABRMode)
        self.channelABRMode = QComboBox()
        self.channelABRMode.addItems(self.listChannels)
        self.ABRWidget.addWidget(self.channelABRMode)
        self.ABRWidget.addStretch()
        self.stackedWidget.addWidget(self.ABRWidget)"""

        self.layout.addStretch()

        #self.makeConnections()

    def defineItems(self):
        self.listBitrateModes = ["CBR (Constant Bitrate)", "VBR (Variable Bitrate)", "ABR (Average Bitrate)"]
        self.listBitrates = "8 16 24 32 40 48 56 64 80 96 112 128 144 160 192 224 256 320".split(" ")
        for i, bitrate in enumerate(self.listBitrates):
            self.listBitrates[i] = bitrate + " kbps"
        self.listQualityLevels = ["Q0 Extreme", "Q1", "Q2 Standart", "Q3", "Q4 Medium", "Q5", "Q6", "Q7", "Q8", "Q9"]
        self.listChannels = ["Joint Stereo", "Stereo", "Mono"]

    def makeConnections(self):
        self.bitrateModeBox.currentIndexChanged.connect(self.stackedWidget.setCurrentIndex)
