from PySide.QtGui import QHBoxLayout, QComboBox, QStackedWidget, QWidget
from PySide.QtCore import QSize, Qt
from EncoderTools import EncoderTools
from GuiTools import HWidget, ComboBox, WidgetList

class EncoderMP3Tools(EncoderTools):

    def __init__(self):
        super().__init__()
        self.bitrateModeWidgets = WidgetList()
        self.defineItems()

        self.layout = QHBoxLayout(self.preferencesWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.bitrateModeBox = ComboBox()
        self.bitrateModeBox.addItems(self.listBitrateModes)
        self.layout.addWidget(self.bitrateModeBox)

        self.CBRWidget = HWidget()
        self.bitrateCBRMode = ComboBox()
        self.bitrateCBRMode.addItems(self.listBitrates)
        self.bitrateCBRMode.setCurrentIndex(14)
        self.CBRWidget.addWidget(self.bitrateCBRMode)
        """self.channelCBRMode = ComboBox()
        self.channelCBRMode.addItems(self.listChannels)
        self.CBRWidget.addWidget(self.channelCBRMode)"""

        self.VBRWidget = HWidget()
        self.qualityVBRMode = ComboBox()
        self.qualityVBRMode.addItems(self.listQualityLevels)
        self.qualityVBRMode.setCurrentIndex(2)
        self.VBRWidget.addWidget(self.qualityVBRMode)
        """self.channelVBRMode = ComboBox()
        self.channelVBRMode.addItems(self.listChannels)
        self.VBRWidget.addWidget(self.channelVBRMode)"""

        self.ABRWidget = HWidget()
        self.bitrateABRMode = ComboBox()
        self.bitrateABRMode.addItems(self.listBitrates)
        self.bitrateABRMode.setCurrentIndex(14)
        self.ABRWidget.addWidget(self.bitrateABRMode)
        """self.channelABRMode = ComboBox()
        self.channelABRMode.addItems(self.listChannels)
        self.ABRWidget.addWidget(self.channelABRMode)"""

        self.layout.addWidget(self.CBRWidget)
        self.bitrateModeWidgets.appendWidget(self.CBRWidget)
        self.layout.addWidget(self.VBRWidget)
        self.bitrateModeWidgets.appendWidget(self.VBRWidget)
        self.layout.addWidget(self.ABRWidget)
        self.bitrateModeWidgets.appendWidget(self.ABRWidget)

        self.layout.addStretch()

        self.bitrateModeWidgets.showOnlyAWidget(self.bitrateModeBox.currentIndex())

        self.makeConnections()

    def defineItems(self):
        self.formatName = "MP3 | MPEG Layer-III"
        self.listBitrateModes = ["CBR (Constant Bitrate)", "VBR (Variable Bitrate)", "ABR (Average Bitrate)"]
        self.listBitrates = "8 16 24 32 40 48 56 64 80 96 112 128 144 160 192 224 256 320".split(" ")
        for i, bitrate in enumerate(self.listBitrates):
            self.listBitrates[i] = bitrate + " kbps"
        self.listQualityLevels = ["Q0 Extreme", "Q1", "Q2 Standart", "Q3", "Q4 Medium", "Q5", "Q6", "Q7", "Q8", "Q9"]
        self.listChannels = ["Joint Stereo", "Stereo", "Mono"]

    def makeConnections(self):
        self.bitrateModeBox.currentIndexChanged.connect(self.bitrateModeWidgets.showOnlyAWidget)