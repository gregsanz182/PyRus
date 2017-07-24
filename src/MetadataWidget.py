from PySide.QtGui import *
from PySide.QtCore import *

class MetadataWidget(QFrame):

    changesSaved = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QFrame#metadataWidget{border-left: 1px solid #ADADAD; background-color: #EEEEEE;}")
        self.setObjectName("metadataWidget")
        self.setFixedWidth(280)
        self.listIndexed = []

        self.metadataLayout = MetadataLayout(self)

        self.titleLabel = QLabel("Title")
        self.titleBox = MetadataTextField("<title>")
        self.metadataLayout.addField(self.titleLabel, self.titleBox)

        self.artistLabel = QLabel("Artist")
        self.artistBox = MetadataTextField("<artist>")
        self.metadataLayout.addField(self.artistLabel, self.artistBox)

        self.albumLabel = QLabel("Album")
        self.albumBox = MetadataTextField("<album>")
        self.metadataLayout.addField(self.albumLabel, self.albumBox)

        self.albumArtistLabel = QLabel("Album Artist")
        self.albumArtistBox = MetadataTextField("<albumartist>")
        self.metadataLayout.addField(self.albumArtistLabel, self.albumArtistBox)

        self.trackLabel = QLabel("Track")
        self.trackBox = MetadataFractionField("<tracknumber>", "<tracktotal>")
        self.trackLayout = MetadataLayout()
        self.trackLayout.addField(self.trackLabel, self.trackBox)

        self.discLabel = QLabel("Disc Number")
        self.discBox = MetadataFractionField("<discnumber>", "<disctotal>")
        self.discLayout = MetadataLayout()
        self.discLayout.addField(self.discLabel, self.discBox)

        self.trackdiscLayout = QHBoxLayout()
        self.trackdiscLayout.addLayout(self.trackLayout)
        self.trackdiscLayout.addLayout(self.discLayout)
        self.trackdiscLayout.setSpacing(20)
        self.metadataLayout.addLayout(self.trackdiscLayout)

        self.commentLabel = QLabel("Comment")
        self.commentBox = MetadataTextField("<comment>")
        self.metadataLayout.addField(self.commentLabel, self.commentBox)

        self.yearLabel = QLabel("Year")
        self.yearBox = MetadataTextField("<year>")
        self.yearBox.setFixedWidth(70)
        self.yearLayout = MetadataLayout()
        self.yearLayout.addField(self.yearLabel, self.yearBox)

        self.genreLabel = QLabel("Genre")
        self.genreBox = MetadataTextField("<genre>")
        self.genreLayout = MetadataLayout()
        self.genreLayout.addField(self.genreLabel, self.genreBox)

        self.yearGenreLayout = QHBoxLayout()
        self.yearGenreLayout.addLayout(self.yearLayout)
        self.yearGenreLayout.addLayout(self.genreLayout)
        self.yearGenreLayout.setSpacing(10)
        self.metadataLayout.addLayout(self.yearGenreLayout)
    
        self.metadataLayout.addStretch()

        self.saveChangesButton = QPushButton("Save Changes")
        self.saveChangesButton.clicked.connect(self.saveChanges)

        self.metadataLayout.addWidget(self.saveChangesButton)


    def setFieldValues(self, listFiles, indexes):
        if len(indexes) > 0:
            self.listIndexed = [listFiles[index.row()] for index in indexes] 
            self.titleBox.setFieldText(self.listIndexed)
            self.artistBox.setFieldText(self.listIndexed)
            self.albumBox.setFieldText(self.listIndexed)
            self.albumArtistBox.setFieldText(self.listIndexed)
            self.yearBox.setFieldText(self.listIndexed)
            self.genreBox.setFieldText(self.listIndexed)
            self.trackBox.setFieldText(self.listIndexed)
            self.discBox.setFieldText(self.listIndexed)
            self.commentBox.setFieldText(self.listIndexed)
        else:
            self.listIndexed.clear()
            self.titleBox.clear()
            self.artistBox.clear()
            self.albumBox.clear()
            self.albumArtistBox.clear()
            self.yearBox.clear()
            self.genreBox.clear()
            self.trackBox.clear()
            self.discBox.clear()
            self.commentBox.clear()

    def saveChanges(self):
        for item in self.listIndexed:
            self.titleBox.setTextToMetadata(item)
            self.artistBox.setTextToMetadata(item)
            self.albumBox.setTextToMetadata(item)
            self.yearBox.setTextToMetadata(item)
            self.genreBox.setTextToMetadata(item)
            self.trackBox.setTextToMetadata(item)
            self.discBox.setTextToMetadata(item)
            self.commentBox.setTextToMetadata(item)
            self.artistBox.setTextToMetadata(item)

        self.changesSaved.emit()

class MetadataLayout(QVBoxLayout):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSpacing(2)

    def addField(self, label=None, widgetField=None):
        self.addWidget(label)
        self.addWidget(widgetField)
        self.addSpacing(5)

class MetadataFractionField(QWidget):

    def __init__(self, metadataItem1=None, metadataItem2=None, parent=None):
        super().__init__(parent)
        self.leftBox = MetadataTextField(metadataItem1)
        self.rightBox = MetadataTextField(metadataItem2)
        self.splitLabel = QLabel("/")
        self.splitLabel.setAlignment(Qt.AlignCenter)
        self.splitLabel.setFixedWidth(4)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 2, 0)
        self.layout.addWidget(self.leftBox)
        self.layout.addWidget(self.splitLabel)
        self.layout.addWidget(self.rightBox)

    def setTextToMetadata(self, item):
        self.leftBox.setTextToMetadata(item)
        self.rightBox.setTextToMetadata(item)

    def setFieldText(self, listIndexed):
        self.leftBox.setFieldText(listIndexed)
        self.rightBox.setFieldText(listIndexed)

    def clear(self):
        self.leftBox.clear()
        self.rightBox.clear()

class MetadataTextField(QComboBox):

    def __init__(self, metadataItem=None, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.metadataItem = metadataItem

    def setFieldText(self, listIndexed):
        textSet = set([item.metadata[self.metadataItem] for item in listIndexed])
        self.updateList(textSet)
        if len(textSet) > 1:
            self.setCurrentIndex(1)
        else:
            self.setCurrentIndex(2)
        self.lineEdit().setCursorPosition(0)

    def obtainTextValue(self, textSet):
        if len(textSet) > 1:
            return "< keep >"
        return list(textSet)[0]

    def updateList(self, textSet):
        textList = ["< delete >", "< keep >"]
        if None in textSet:
            textSet.remove(None)
            textSet.add("")
        aux = list(textSet)
        aux.sort()
        textList.extend(aux)
        self.clear()
        self.addItems(textList)

    def setTextToMetadata(self, item):
        if self.metadataItem is not None:
            if self.currentText() != "< keep >":
                if self.currentText() == "< delete >":
                    item.metadata[self.metadataItem] = None
                else:
                    item.metadata[self.metadataItem] = self.currentText()
