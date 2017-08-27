import os
from PySide.QtGui import QFrame, QVBoxLayout, QHBoxLayout, \
QLineEdit, QToolButton, QIcon, QLabel, QFileDialog, QCheckBox, \
QSpinBox, QSizePolicy
from PySide.QtCore import QSize, Qt
from EncoderMP3Tools import EncoderMP3Tools
from EncoderFLACTools import EncoderFLACTools
from GuiTools import CustomComboBox, WidgetList, CheckFormWidget, CustomHFormLayout

class BottomFrame(QFrame):
    """Bottom Frame of the application.
    Provides the set of items that handles the preferences of conversion and output"""

    def __init__(self, parent=None):
        """Constructor of the class"""
        super().__init__(parent)
        self.setStyleSheet("QFrame#bottomFrame {border-top: 1px solid #ADADAD; background-color: #EEEEEE;}")
        self.setObjectName("bottomFrame")
        self.setFixedHeight(120)
        self.initComponents()

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(45)
        self.setOutputPreferencesLayout()
        self.setSecondColumnLayout()
        self.layout.addStretch()
        self.setStartLayout()

        #self.makeConnections()

    def initComponents(self):
        """Initializes the components"""
        #Encoders Tools initialization
        self.encodersTools = []
        self.encodersTools.append(EncoderMP3Tools())
        self.encodersTools.append(EncoderFLACTools())

    def setOutputPreferencesLayout(self):
        """Sets the layout that contains the items that handles the format preferences"""
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

    def setSecondColumnLayout(self):
        #Second ColumnLayout
        self.secondColumnLayout = QVBoxLayout()
        self.secondColumnLayout.setContentsMargins(0, 2, 0, 10)
        self.secondColumnLayout.setSpacing(3)
        self.layout.addLayout(self.secondColumnLayout)

        #Layout that contains the format combo box and the preferences button
        self.formatLayout = QHBoxLayout()
        self.formatLayout.setContentsMargins(0, 0, 0, 0)
        self.formatLayout.setSpacing(5)
        self.secondColumnLayout.addWidget(QLabel("Output Format"))
        self.secondColumnLayout.addLayout(self.formatLayout)

        #Format Layout elements
        self.formatBox = CustomComboBox()
        for encoderTool in self.encodersTools:
            self.formatBox.addItem(encoderTool.formatName, encoderTool)
        self.formatLayout.addWidget(self.formatBox)
        self.formatPrefButton = QToolButton()
        self.formatPrefButton.setIcon(QIcon("resources\\imgs\\formatPreferencesIcon.png"))
        self.formatPrefButton.setFixedSize(QSize(25, 25))
        self.formatLayout.addWidget(self.formatPrefButton)

        self.secondColumnLayout.addStretch()

        #Other output preferences
        self.overwriteCheckBox = QCheckBox("Overwrite existing files")
        self.removeConvertedCheckBox = QCheckBox("Remove converted files from the list")
        self.secondColumnLayout.addWidget(self.overwriteCheckBox)
        self.secondColumnLayout.addWidget(self.removeConvertedCheckBox)

    def setStartLayout(self):
        """Sets the layout that contains the start button and other preferences."""
        self.startLayout = QVBoxLayout()
        self.startLayout.setContentsMargins(0, 0, 0, 5)
        self.startLayout.setSpacing(5)
        self.layout.addLayout(self.startLayout)

        self.startLayout.addStretch()

        #Layout that contains QSpinBox
        self.convertersLayout = QHBoxLayout()
        self.convertersLayout.setContentsMargins(0, 0, 0, 0)
        self.convertersLayout.setSpacing(6)
        self.startLayout.addLayout(self.convertersLayout)
        self.convertersLayout.addWidget(QLabel("Number of parallel conversions"))
        self.numberConverters = QSpinBox()
        self.numberConverters.setMinimum(1)
        self.numberConverters.setMaximum(5)
        self.numberConverters.setValue(1)
        self.numberConverters.setFixedSize(QSize(37, 23))
        self.convertersLayout.addWidget(self.numberConverters)

        #Start Button
        self.startButton = QToolButton()
        self.startButton.setIcon(QIcon("resources/imgs/startConvert.png"))
        self.startButton.setIconSize(QSize(59, 29))
        self.startButton.setText("Start Conversion")
        self.startButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.startButton.setFixedHeight(55)
        self.startButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.startLayout.addWidget(self.startButton)


    def makeConnections(self):
        """Makes the connections between the signals and slots of the frame components."""
        self.formatBox.currentIndexChanged.connect(self.formatWidgets.showOnlyAWidget)
        self.outputFolderButton.clicked.connect(self.selectOutputFolder)

    def selectOutputFolder(self):
        """Opens a QFileDialog that allows the selection of the output folder"""
        path = QFileDialog.getExistingDirectory(self, "Select Folder", os.getcwd())
        if len(path) > 0:
            self.outputFolderText.setText(path)

    def getOutputPreferences(self) -> tuple:
        """Returns the output preferences as a Tuple. The first position is the
        output folder and the second position is the file name template"""
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
        """Returns the active tool"""
        if self.formatBox.currentIndex() == 0:
            return self.flactools
        elif self.formatBox.currentIndex() == 1:
            return self.mp3tools
