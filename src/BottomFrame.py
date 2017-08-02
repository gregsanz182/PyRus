from PySide.QtGui import QFrame, QVBoxLayout, QComboBox, QHBoxLayout, QStackedLayout, QStackedWidget, \
QSizePolicy, QCheckBox, QFormLayout, QLineEdit, QToolButton, QIcon, QLabel
from PySide.QtCore import Qt, QSize
from EncoderMP3Tools import EncoderMP3Tools
from EncoderFLACTools import EncoderFLACTools
from GuiTools import ComboBox, WidgetList, CustomVFormLayout, CheckFormWidget, CustomHFormLayout

class BottomFrame(QFrame):

    def __init__(self, parent=None):
        """Top Frame of the application. 
        Provides the set of times that handles the preferences of conversion and output"""
        super().__init__(parent)
        self.setStyleSheet("QFrame#bottomFrame {border-top: 1px solid #ADADAD; background-color: #EEEEEE;}")
        self.setObjectName("bottomFrame")
        self.setFixedHeight(120)
        self.initComponents()

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(30)
        self.setOutputPreferencesLayout()
        self.setFormatPreferencesWidget()
        self.layout.addStretch()

        self.makeConnections()

    def initComponents(self):
        self.mp3tools = EncoderMP3Tools()
        self.flactools = EncoderFLACTools()
        
    def setFormatPreferencesWidget(self):
        self.formatWidgets = WidgetList()
        self.formatLayout = QVBoxLayout()
        self.formatLayout.setSpacing(6)
        self.layout.addLayout(self.formatLayout)

        self.formatBox = ComboBox()
        self.formatLayoutTop = CustomHFormLayout()
        self.formatLayout.addLayout(self.formatLayoutTop)
        self.formatLayoutTop.addField(QLabel("Ouput Format"), self.formatBox)
        self.formatLayoutTop.addStretch()

        self.formatBox.addItem(self.flactools.formatName)
        self.formatLayout.addWidget(self.flactools.preferencesWidget)
        self.formatWidgets.appendWidget(self.flactools.preferencesWidget)

        self.formatBox.addItem(self.mp3tools.formatName)
        self.formatLayout.addWidget(self.mp3tools.preferencesWidget)
        self.formatWidgets.appendWidget(self.mp3tools.preferencesWidget)

        self.formatWidgets.showOnlyAWidget(self.formatBox.currentIndex())

        self.formatLayout.addStretch()

    def setOutputPreferencesLayout(self):
        self.outputLayout = QVBoxLayout()
        self.outputLayout.setContentsMargins(0, 0, 0, 0)
        self.outputLayout.setSpacing(6)
        self.layout.addLayout(self.outputLayout)
        
        self.outputFolderText = QLineEdit()
        self.outputFolderText.setFixedHeight(23)
        self.outputFolderButton = QToolButton()
        self.outputFolderButton.setIcon(QIcon("resources/imgs/searchFolder.png"))
        self.outputFolderButton.setFixedSize(QSize(25, 25))
        self.outputFolderWidget = CheckFormWidget(self.outputFolderText, self.outputFolderButton, "Set Output Folder")
        self.outputLayout.addWidget(self.outputFolderWidget)

        self.fileNameText = QLineEdit()
        self.fileNameText.setFixedHeight(23)
        self.fileNameButton = QToolButton()
        self.fileNameButton.setIcon(QIcon("resources/imgs/editTemplateText.png"))
        self.fileNameButton.setFixedSize(QSize(25, 25))
        self.fileNameWidget = CheckFormWidget(self.fileNameText, self.fileNameButton, "Set Filename")
        self.outputLayout.addWidget(self.fileNameWidget)

        self.outputLayout.addStretch()

    def makeConnections(self):
        self.formatBox.currentIndexChanged.connect(self.formatWidgets.showOnlyAWidget)
