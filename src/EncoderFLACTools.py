from PySide.QtGui import QLabel
from EncoderTools import EncoderTools
from GuiTools import CustomComboBox, CustomHFormLayout
from FileAudio import FileAudio
from Tools import CustomProcess

class EncoderFLACTools(EncoderTools):
    """Provides Tools like Widgets, methods and objects for the FLAC encoder."""

    def __init__(self):
        """Constructor of the class"""
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
        """Defines the tool items."""
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

    def defineTagsMapping(self):
        """Defines the mapping of the tags needed for the use in the encoder CLI"""
        self.tagsMapping["<title>"] = "TITLE"
        self.tagsMapping["<albumartist>"] = "ALBUMARTIST"
        self.tagsMapping["<artist>"] =  "ARTIST"
        self.tagsMapping["<album>"] = "ALBUM"
        self.tagsMapping["<tracknumber>"] = "TRACKNUMBER"
        self.tagsMapping["<tracktotal>"] = "TOTALTRACKS"
        self.tagsMapping["<discnumber>"] = "DISCNUMBER"
        self.tagsMapping["<disctotal>"] = "TOTALDISCS"
        self.tagsMapping["<genre>"] = "GENRE"
        self.tagsMapping["<year>"] = "YEAR"
        self.tagsMapping["<comment>"] = "COMMENT"
        self.tagsMapping["<lyrics>"] = "LYRICS"

    def prepareProcess(self, audioFile: FileAudio, outputPath: str) -> CustomProcess:
        """Returns the CustomProcess with commandline arguments defined"""
        process = CustomProcess()
        process.setProgram("resources\\tools\\flac")
        process.extendArg(["--totally-silent", "-f", "--ignore-chunk-sizes"])
        if self.containerBox.currentIndex() == 1:
            process.appendArg("--ogg")
        process.appendArg("-"+self.compressionLevels[self.compressionLevelBox.currentIndex()])
        if audioFile.metadata["<coverfile>"] and audioFile.metadata["<covermime>"]:
            process.appendArg("--picture=3|{0}|||{1}".format(audioFile.metadata["<covermime>"], audioFile.metadata["<coverfile>"]))
        process.extendArg(self.getTagArgs(audioFile))
        process.appendArg('--output-name={0}'.format(outputPath))
        process.appendArg("-")
        
        return process

    def getTagArgs(self, audioFile: FileAudio) -> list:
        """Returns the tags values formatted for the use in the CLI. Recieves the audioFile
        with its corresponding tags"""
        args = []
        for field, value in audioFile.metadata.items():
            if field in self.tagsMapping and value is not None:
                args.append('--tag={0}={1}'.format(self.tagsMapping[field], value))
        return args

    def getExtension(self) -> str:
        """Returns the extension selected in the GUI"""
        if self.containerBox.currentIndex() == 1:
            return ".ogg"
        return ".flac"
