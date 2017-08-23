from PySide.QtGui import QFrame, QVBoxLayout, QHBoxLayout, \
QLineEdit, QToolButton, QIcon, QLabel, QFileDialog
from PySide.QtCore import QSize, Qt
from EncoderMP3Tools import EncoderMP3Tools
from EncoderFLACTools import EncoderFLACTools
from GuiTools import CustomComboBox, WidgetList, CheckFormWidget, CustomHFormLayout
import os

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
        self.setFormatPreferencesLayout()
        self.layout.addStretch()
        self.setStartButton()

        self.makeConnections()

    def initComponents(self):
        self.mp3tools = EncoderMP3Tools()
        self.flactools = EncoderFLACTools()
        
    def setFormatPreferencesLayout(self):
        self.formatWidgets = WidgetList()
        self.formatLayout = QVBoxLayout()
        self.formatLayout.setSpacing(6)
        self.layout.addLayout(self.formatLayout)

        self.formatBox = CustomComboBox()
        self.formatLayoutTop = CustomHFormLayout()
        self.formatLayout.addLayout(self.formatLayoutTop)
        self.formatLayoutTop.addField(QLabel("Output Format"), self.formatBox)

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

    def setStartButton(self):
        self.startButton = QToolButton()
        self.startButton.setIcon(QIcon("resources/imgs/startConvert.png"))
        self.startButton.setIconSize(QSize(59, 29))
        self.startButton.setText("Start Conversion")
        self.startButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.startButton.setStyleSheet("QToolButton {padding: 0px 16px 7px 16px;}")
        #self.startButton.setFixedWidth(80)
        self.layout.addWidget(self.startButton, alignment=Qt.AlignBottom)

    def makeConnections(self):
        self.formatBox.currentIndexChanged.connect(self.formatWidgets.showOnlyAWidget)
        self.outputFolderButton.clicked.connect(self.selectOutputFolder)

    def selectOutputFolder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder", os.getcwd())
        if len(path) > 0:
            self.outputFolderText.setText(path)

    def getOutputPreferences(self) -> tuple:
        if self.fileNameWidget.getState() is Qt.Checked:
            template = self.fileNameText.text()
        else:
            template = ""
        if self.outputFolderWidget.getState() is Qt.Checked:
            folder = self.outputFolderText.text()
        else:
            folder = ""
        return tuple([folder, template])

    def getTool(self):
        if self.formatBox.currentIndex() == 0:
            return self.flactools
        elif self.formatBox.currentIndex() == 1:
            return self.mp3tools
