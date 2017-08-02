from PySide.QtGui import QHBoxLayout, QComboBox, QStackedWidget, QWidget, QLabel
from PySide.QtCore import QSize, Qt
from EncoderTools import EncoderTools
from GuiTools import HWidget, ComboBox, WidgetList, CustomHFormLayout

class EncoderMP3Tools(EncoderTools):

    def __init__(self):
        super().__init__()
        self.bitrateModeWidgets = WidgetList()
        self.defineItems()

        self.layout = CustomHFormLayout(self.preferencesWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.bitrateModeBox = ComboBox()
        self.bitrateModeBox.addItems(self.listBitrateModes)
        self.layout.addField(QLabel("Bitrate mode"), self.bitrateModeBox)

        self.CBRWidget = QWidget()
        self.CBRWidget.setLayout(CustomHFormLayout())
        self.CBRWidget.layout().setContentsMargin(0)
        self.bitrateCBRBox = ComboBox()
        self.bitrateCBRBox.addItems(self.listBitrates)
        self.bitrateCBRBox.setCurrentIndex(14)
        self.CBRWidget.layout().addField(QLabel("Bitrate"), self.bitrateCBRBox)
        """self.channelCBRMode = ComboBox()
        self.channelCBRMode.addItems(self.listChannels)
        self.CBRWidget.addWidget(self.channelCBRMode)"""

        self.VBRWidget = QWidget()
        self.VBRWidget.setLayout(CustomHFormLayout())
        self.VBRWidget.layout().setContentsMargin(0)
        self.qualityVBRBox = ComboBox()
        self.qualityVBRBox.addItems(self.listQualityLevels)
        self.qualityVBRBox.setCurrentIndex(2)
        self.VBRWidget.layout().addField(QLabel("Quality Level"), self.qualityVBRBox)
        """self.channelVBRMode = ComboBox()
        self.channelVBRMode.addItems(self.listChannels)
        self.VBRWidget.addWidget(self.channelVBRMode)"""

        self.ABRWidget = QWidget()
        self.ABRWidget.setLayout(CustomHFormLayout())
        self.ABRWidget.layout().setContentsMargin(0)
        self.bitrateABRBox = ComboBox()
        self.bitrateABRBox.addItems(self.listBitrates)
        self.bitrateABRBox.setCurrentIndex(14)
        self.ABRWidget.layout().addField(QLabel("Bitrate"), self.bitrateABRBox)
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