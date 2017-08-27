from PySide.QtGui import QWidget, QLabel
from EncoderTools import EncoderTools
from GuiTools import CustomComboBox, WidgetList, CustomHFormLayout
from FileAudio import FileAudio
from Tools import CustomProcess

class EncoderMP3Tools(EncoderTools):
    """Provides Tools like Widgets, methods and objects for the MP3 encoder."""

    def __init__(self):
        """Constructor of the class"""
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
        """Defines the tool items."""
        self.formatName = "MP3 | MPEG Layer-III"
        self.listBitrateModes = ["CBR (Constant Bitrate)", "VBR (Variable Bitrate)", "ABR (Average Bitrate)"]
        self.listBitrates = "8 16 24 32 40 48 56 64 80 96 112 128 144 160 192 224 256 320".split(" ")
        self.listBitratesText = []
        for bitrate in self.listBitrates:
            self.listBitratesText.append(bitrate + " kbps")
        self.listQualityLevels = ["Q0 Extreme", "Q1", "Q2 Standart", "Q3", "Q4 Medium", "Q5", "Q6", "Q7", "Q8", "Q9"]
        self.listChannels = ["Joint Stereo", "Stereo", "Mono"]

    def defineTagsMapping(self):
        """Defines the mapping of the tags needed for the use in the encoder CLI"""
        self.tagsMapping["<title>"] = "TIT2"
        self.tagsMapping["<albumartist>"] = "TPE2"
        self.tagsMapping["<artist>"] =  "TPE1"
        self.tagsMapping["<album>"] = "TALB"
        self.tagsMapping["<genre>"] = "TCON"
        self.tagsMapping["<year>"] = "TYER"
        self.tagsMapping["<comment>"] = "COMM"

    def makeConnections(self):
        """Makes the connection between the signals and slots of the GUI components"""
        self.bitrateModeBox.currentIndexChanged.connect(self.bitrateModeWidgets.showOnlyAWidget)

    def prepareProcess(self, audioFile: FileAudio, outputPath: str) -> CustomProcess:
        """Returns the CustomProcess with commandline arguments defined"""
        process = CustomProcess()
        process.setProgram("resources\\tools\\lame")
        process.extendArg(self.getBitrateModeArgs())
        process.extendArg(self.getTagArgs(audioFile))
        if audioFile.metadata["<coverfile>"]:
            process.extendArg(["--ti", str(audioFile.metadata["<coverfile>"])])
        process.extendArg(["--ignorelength", "--verbose", "-", outputPath])
        return process

    def getExtension(self) -> str:
        """Returns the extension selected in the GUI"""
        return ".mp3"

    def getBitrateModeArgs(self) -> list:
        if self.bitrateModeBox.currentIndex() == 0:
            return ["--cbr", "-b", str(self.listBitrates[self.bitrateCBRBox.currentIndex()])]
        elif self.bitrateModeBox.currentIndex() == 1:
            return ["--vbr-new", "-V", str(self.qualityVBRBox.currentIndex())]
        elif self.bitrateModeBox.currentIndex() == 2:
            return ["--abr", str(self.listBitrates[self.bitrateABRBox.currentIndex()])]

    def getTagArgs(self, audioFile: FileAudio) -> list:
        """Returns the tags values formatted for the use in the CLI. Recieves the audioFile
        with its corresponding tags"""
        args = []
        for field, value in audioFile.metadata.items():
            if field in self.tagsMapping and value is not None:
                args.extend(['--tv', '{0}={1}'.format(self.tagsMapping[field], value)])
        tdn = ""
        if audioFile.metadata["<tracknumber>"]:
            tdn += audioFile.metadata["<tracknumber>"]
        if audioFile.metadata["<tracktotal>"]:
            tdn += "/"+audioFile.metadata["<tracktotal>"]
        if tdn != "":
            args.extend(['--tv', 'TRCK={0}'.format(tdn)])
        return args
