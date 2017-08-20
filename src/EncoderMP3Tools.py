from PySide.QtGui import QWidget, QLabel
from EncoderTools import EncoderTools
from GuiTools import CustomComboBox, WidgetList, CustomHFormLayout
from FileAudio import FileAudio

class EncoderMP3Tools(EncoderTools):

    def __init__(self):
        super().__init__()
        self.bitrateModeWidgets = WidgetList()

        self.layout = CustomHFormLayout(self.preferencesWidget)
        self.layout.setContentsMargin(0)

        self.bitrateModeBox = CustomComboBox()
        self.bitrateModeBox.addItems(self.listBitrateModes)
        self.layout.addField(QLabel("Bitrate mode"), self.bitrateModeBox)

        self.CBRWidget = QWidget()
        self.CBRWidget.setLayout(CustomHFormLayout())
        self.CBRWidget.layout().setContentsMargin(0)
        self.bitrateCBRBox = CustomComboBox()
        self.bitrateCBRBox.addItems(self.listBitratesText)
        self.bitrateCBRBox.setCurrentIndex(14)
        self.CBRWidget.layout().addField(QLabel("Bitrate"), self.bitrateCBRBox)
        """self.channelCBRMode = CustomComboBox()
        self.channelCBRMode.addItems(self.listChannels)
        self.CBRWidget.addWidget(self.channelCBRMode)"""

        self.VBRWidget = QWidget()
        self.VBRWidget.setLayout(CustomHFormLayout())
        self.VBRWidget.layout().setContentsMargin(0)
        self.qualityVBRBox = CustomComboBox()
        self.qualityVBRBox.addItems(self.listQualityLevels)
        self.qualityVBRBox.setCurrentIndex(2)
        self.VBRWidget.layout().addField(QLabel("Quality Level"), self.qualityVBRBox)
        """self.channelVBRMode = CustomComboBox()
        self.channelVBRMode.addItems(self.listChannels)
        self.VBRWidget.addWidget(self.channelVBRMode)"""

        self.ABRWidget = QWidget()
        self.ABRWidget.setLayout(CustomHFormLayout())
        self.ABRWidget.layout().setContentsMargin(0)
        self.bitrateABRBox = CustomComboBox()
        self.bitrateABRBox.addItems(self.listBitrates)
        self.bitrateABRBox.setCurrentIndex(14)
        self.ABRWidget.layout().addField(QLabel("Bitrate"), self.bitrateABRBox)
        """self.channelABRMode = CustomComboBox()
        self.channelABRMode.addItems(self.listChannels)
        self.ABRWidget.addWidget(self.channelABRMode)"""

        self.layout.addWidget(self.CBRWidget)
        self.bitrateModeWidgets.appendWidget(self.CBRWidget)
        self.layout.addWidget(self.VBRWidget)
        self.bitrateModeWidgets.appendWidget(self.VBRWidget)
        self.layout.addWidget(self.ABRWidget)
        self.bitrateModeWidgets.appendWidget(self.ABRWidget)

        self.bitrateModeWidgets.showOnlyAWidget(self.bitrateModeBox.currentIndex())

        self.makeConnections()

    def defineItems(self):
        self.formatName = "MP3 | MPEG Layer-III"
        self.listBitrateModes = ["CBR (Constant Bitrate)", "VBR (Variable Bitrate)", "ABR (Average Bitrate)"]
        self.listBitrates = "8 16 24 32 40 48 56 64 80 96 112 128 144 160 192 224 256 320".split(" ")
        self.listBitratesText = []
        for bitrate in self.listBitrates:
            self.listBitratesText.append(bitrate + " kbps")
        self.listQualityLevels = ["Q0 Extreme", "Q1", "Q2 Standart", "Q3", "Q4 Medium", "Q5", "Q6", "Q7", "Q8", "Q9"]
        self.listChannels = ["Joint Stereo", "Stereo", "Mono"]

    def defineTagsMapping(self):
        pass

    def makeConnections(self):
        self.bitrateModeBox.currentIndexChanged.connect(self.bitrateModeWidgets.showOnlyAWidget)

    def prepareCMDLine(self, audioFile: FileAudio):
        pass