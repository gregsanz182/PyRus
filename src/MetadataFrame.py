from PySide.QtGui import *
from PySide.QtCore import *
from os import path

class MetadataFrame(QFrame):
    """Metadata Frame of the application. Provides fields that shows details of the files selected,
    and allows the managing of the tags. Here, the user can modify the tags of the files selected."""

    changesSaved = Signal()

    def __init__(self, parent=None):
        """Constructor of the class. Initializes and sets all the components"""
        super().__init__(parent)
        self.setStyleSheet("QFrame#metadataFrame{border-left: 1px solid #ADADAD; background-color: #EEEEEE;}")
        self.setObjectName("metadataFrame")
        self.setFixedWidth(320)
        self.listIndexed = []

        self.metadataLayout = MetadataLayout(self)

        self.coverWidget = MetadataCoverWidget()
        self.metadataLayout.addWidget(self.coverWidget)
        self.metadataLayout.addSpacing(5)
        self.metadataLayout.addSeparator()

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
        """Sets the values of all the fields given the 'listFiles' and the index of the items selected"""
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
            self.coverWidget.setCover(self.listIndexed)
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
            self.coverWidget.setNoCover()

    def saveChanges(self):
        """Save the changes in the list and emits the signal 'changesSaved'"""
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

class MetadataCoverWidget(QWidget):
    """Widget that provides a QLabel for showing the cover of the file selected and buttons for
    change, remove and export cover"""

    def __init__(self, parent=None):
        """Constructor of the class. Initializes and sets all the components"""
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.coverLabel = QLabel()
        self.coverLabel.setFixedSize(QSize(150, 150))
        self.coverLabel.setStyleSheet("QLabel#coverLabel {border: 1px solid #ADADAD; background-color: #FFFFFF;}")
        self.coverLabel.setObjectName("coverLabel")
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor("#CCCCCC"))
        shadow.setOffset(2, 2)
        shadow.setBlurRadius(15)
        self.coverLabel.setGraphicsEffect(shadow)
        self.defaultCover = QPixmap("resources//imgs//nocover.png").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.layout.addWidget(self.coverLabel, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(3)

        self.detailLabel = QLabel("")
        self.layout.addWidget(self.detailLabel, alignment=Qt.AlignHCenter)
        self.layout.addSpacing(5)
        
        self.setButtons()

        self.setNoCover()

    def setCover(self, listIndexed):
        """Sets the cover (of the files selected) in the coverLabel for showing"""
        coverSet = set(item.metadata["<coverfile>"] for item in listIndexed)
        if len(coverSet) > 1:
            self.coverLabel.setPixmap(self.defaultCover)
            self.detailLabel.setText("Covers varies")
        else:
            pixmap, detail = listIndexed[0].getCoverWithInfo()
            if pixmap is None:
                self.coverLabel.setPixmap(self.defaultCover)
            else:
                self.coverLabel.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.detailLabel.setText(detail)

    def setNoCover(self):
        """Sets the default cover"""
        self.coverLabel.setPixmap(self.defaultCover)
        self.detailLabel.setText("")

    def setButtons(self):
        """Initializes and sets the buttons corresponding to 'change', 'remove' and 'export' functionalities"""
        self.changeButton = QPushButton("Change...")
        self.removeButton = QPushButton("Remove...")
        self.exportButton = QPushButton("Export...")

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setSpacing(10)
        self.buttonsLayout.setContentsMargins(10, 0,10, 0)
        self.layout.addLayout(self.buttonsLayout)

        self.buttonsLayout.addWidget(self.changeButton)
        self.buttonsLayout.addWidget(self.removeButton)
        self.buttonsLayout.addWidget(self.exportButton)

class MetadataLayout(QVBoxLayout):
    """Custom Layout of the MetadataFrame. Arranges every item like a form, but with label above the text field.
    Extends QVBoxLayout"""

    def __init__(self, parent=None):
        """Constructor of the class. Initializes and sets all the components"""
        super().__init__(parent)
        self.setSpacing(2)

    def addField(self, label=None, widgetField=None):
        """Adds the given label and widget in the layout"""
        self.addWidget(label)
        self.addWidget(widgetField)
        self.addSpacing(5)

    def addSeparator(self):
        """Adds a separator to the layout"""
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.addSpacing(5)
        self.addWidget(separator)
        self.addSpacing(5)

class MetadataFractionField(QWidget):
    """A Custom field consisting of two QComboBox and a slash between them."""

    def __init__(self, metadataItem1=None, metadataItem2=None, parent=None):
        """Constructor of the class. Initializes and sets all the components"""
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
        """Sets the current text in the fields to the metadata of the file list"""
        self.leftBox.setTextToMetadata(item)
        self.rightBox.setTextToMetadata(item)

    def setFieldText(self, listIndexed):
        """Sets the metadata values in the fields"""
        self.leftBox.setFieldText(listIndexed)
        self.rightBox.setFieldText(listIndexed)

    def clear(self):
        """Cleans the Combo boxes"""
        self.leftBox.clear()
        self.rightBox.clear()

class MetadataTextField(QComboBox):
    """A Custom QComboBox for the display and editing of the values in the metadata of the fileList"""

    def __init__(self, metadataItem=None, parent=None):
        """Constructor of the class. Initializes and sets all the components"""
        super().__init__(parent)
        self.setEditable(True)
        self.metadataItem = metadataItem

    def setFieldText(self, listIndexed):
        """Sets the value of the tags in listIndexed to the fields.
        If values varies, '< keep >' is set"""
        textSet = set([item.metadata[self.metadataItem] for item in listIndexed])
        self.updateList(textSet)
        if len(textSet) > 1:
            self.setCurrentIndex(1)
        else:
            self.setCurrentIndex(2)
        self.lineEdit().setCursorPosition(0)

    def obtainTextValue(self, textSet):
        """Returns either '< keep >' or the tags value depending on the simililarities of the content"""
        if len(textSet) > 1:
            return "< keep >"
        return list(textSet)[0]

    def updateList(self, textSet):
        """Updates the list of the QComboBox with the values of the selected items"""
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
        """Sets the current value of 'item' in the metadata tags of the file"""
        if self.metadataItem is not None:
            if self.currentText() != "< keep >":
                if self.currentText() == "< delete >":
                    item.metadata[self.metadataItem] = None
                else:
                    item.metadata[self.metadataItem] = self.currentText()
