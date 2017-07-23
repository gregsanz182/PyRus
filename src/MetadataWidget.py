from PySide.QtGui import *
from PySide.QtCore import *

class MetadataWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QFrame {border-left: 1px solid #ADADAD; background-color: #EEEEEE;}")
        self.setFixedWidth(280)

        self.metadataLayout = MetadataLayout(self)

        self.titleLabel = MetadataLabel("Title")
        self.titleBox = MetadataTextField()
        self.titleBox.setEditable(True)
        self.metadataLayout.addField(self.titleLabel, self.titleBox)

        self.artistLabel = MetadataLabel("Artist")
        self.artistBox = MetadataTextField()
        self.artistBox.setEditable(True)
        self.metadataLayout.addField(self.artistLabel, self.artistBox)

        self.albumLabel = MetadataLabel("Album")
        self.albumBox = MetadataTextField()
        self.albumBox.setEditable(True)
        self.metadataLayout.addField(self.albumLabel, self.albumBox)
        
        self.yearLabel = MetadataLabel("Year")
        self.yearBox = MetadataTextField()
        self.yearBox.setEditable(True)
        self.yearBox.setMaximumWidth(80)
        self.yearLayout = MetadataLayout()
        self.yearLayout.addField(self.yearLabel, self.yearBox)

        self.genreLabel = MetadataLabel("Genre")
        self.genreBox = MetadataTextField()
        self.genreBox.setEditable(True)
        self.genreLayout = MetadataLayout()
        self.genreLayout.addField(self.genreLabel, self.genreBox)

        self.yearGenreLayout = QHBoxLayout()
        self.yearGenreLayout.addLayout(self.yearLayout)
        self.yearGenreLayout.addLayout(self.genreLayout)
        self.yearGenreLayout.setSpacing(10)
        self.metadataLayout.addLayout(self.yearGenreLayout)
        
        self.metadataLayout.addStretch()

    def setFieldValues(self, listFiles, indexes):
        if len(indexes) > 0:
            listIndexed = [listFiles[index.row()] for index in indexes] 
            self.titleBox.setFieldText(set([item.metadata["<title>"] for item in listIndexed]))
            self.artistBox.setFieldText(set([item.metadata["<artist>"] for item in listIndexed]))
            self.albumBox.setFieldText(set([item.metadata["<album>"] for item in listIndexed]))
            self.yearBox.setFieldText(set([item.metadata["<year>"] for item in listIndexed]))
            self.genreBox.setFieldText(set([item.metadata["<genre>"] for item in listIndexed]))
        else:
            self.titleBox.clear()
            self.artistBox.clear()
            self.albumBox.clear()
            self.yearBox.clear()
            self.genreBox.clear()


class MetadataLayout(QVBoxLayout):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSpacing(2)

    def addField(self, label=None, textField=None):
        self.addWidget(label)
        self.addWidget(textField)
        self.addSpacing(5)

class MetadataLabel(QLabel):

    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("QLabel {border: 0px;}")

class MetadataTextField(QComboBox):

    def __init__(self, parent=None, customList=None):
        super().__init__(parent)
        self.setEditable(True)

    def setFieldText(self, textSet):
        self.updateListModel(textSet)
        if len(textSet) > 1:
            self.setCurrentIndex(1)
        else:
            self.setCurrentIndex(2)

    def obtainTextValue(self, textSet):
        if len(textSet) > 1:
            return "< keep >"
        return list(textSet)[0]

    def updateListModel(self, textSet):
        textList = ["< delete >", "< keep >"]
        aux = list(textSet)
        aux.sort()
        textList.extend(aux)
        self.clear()
        self.addItems(textList)


