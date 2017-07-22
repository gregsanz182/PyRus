from PySide.QtGui import *
from PySide.QtCore import *

class MetadataWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QFrame {border-left: 1px solid #ADADAD; background-color: #EEEEEE;}")
        self.setMaximumWidth(280)

        self.metadataLayout = MetadataLayout(self)

        self.titleLabel = MetadataLabel("Title")
        self.titleText = QLineEdit()
        self.metadataLayout.addField(self.titleLabel, self.titleText)

        self.artistLabel = MetadataLabel("Artist")
        self.artistText = QLineEdit()
        self.metadataLayout.addField(self.artistLabel, self.artistText)

        self.albumLabel = MetadataLabel("Album")
        self.albumText = QLineEdit()
        self.metadataLayout.addField(self.albumLabel, self.albumText)
        
        self.yearLabel = MetadataLabel("Year")
        self.yearText = QLineEdit()
        self.yearText.setMaximumWidth(80)
        self.yearLayout = MetadataLayout()
        self.yearLayout.addField(self.yearLabel, self.yearText)

        self.genreLabel = MetadataLabel("Genre")
        self.genreText = QLineEdit()
        self.genreLayout = MetadataLayout()
        self.genreLayout.addField(self.genreLabel, self.genreText)

        self.yearGenreLayout = QHBoxLayout()
        self.yearGenreLayout.addLayout(self.yearLayout)
        self.yearGenreLayout.addLayout(self.genreLayout)
        self.yearGenreLayout.setSpacing(10)
        self.metadataLayout.addLayout(self.yearGenreLayout)
        
        self.metadataLayout.addStretch()

    def setFieldValues(self, listFiles, indexes):
        if len(indexes) > 0:
            self.titleText.setText(listFiles[indexes[0].row()].title)
            self.artistText.setText(listFiles[indexes[0].row()].artist)
            self.albumText.setText(listFiles[indexes[0].row()].album)
            self.yearText.setText(listFiles[indexes[0].row()].year)
            self.genreText.setText(listFiles[indexes[0].row()].genre)
        else:
            self.titleText.setText("")
            self.artistText.setText("")
            self.albumText.setText("")
            self.yearText.setText("")
            self.genreText.setText("")


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
