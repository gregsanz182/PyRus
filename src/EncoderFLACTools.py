from PySide.QtGui import QLabel
from EncoderTools import EncoderTools
from GuiTools import CustomComboBox, CustomHFormLayout
from FileAudio import FileAudio
from CustomProcess import CustomProcess

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

    def defineTagsMapping(self):
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

    def prepareProcess(self, audioFile: FileAudio) -> CustomProcess:
        process = CustomProcess()
        process.setProgram("resources\\tools\\flac")
        process.appendArg("--totally-silent")
        if self.containerBox.currentIndex() == 1:
            process.appendArg("--ogg")
        process.appendArg("-"+self.compressionLevels[self.compressionLevelBox.currentIndex()])
        """if audioFile.metadata["<coverfile>"] is not None:
            cmdline += " --picture=3|"
            if audioFile.metadata["<covermime>"] is not None:
                cmdline += audioFile.metadata["<covermime>"]
            cmdline += "|||"
            cmdline += audioFile.metadata["<coverfile>"]"""
        
        process.extendArg(self.getTagArgs(audioFile))
        process.appendArg('--output-name=test.flac')
        process.appendArg("-")

        for arg in process.args:
            print(arg)
        return process

    def getTagArgs(self, audioFile) -> list:
        args = []
        for field, value in audioFile.metadata.items():
            if field in self.tagsMapping and value is not None:
                args.append('--tag={0}={1}'.format(self.tagsMapping[field], value))
        return args    
