from PySide.QtGui import QFrame, QVBoxLayout, QComboBox, QHBoxLayout, QStackedLayout, QStackedWidget, QSizePolicy
from EncoderMP3Tools import EncoderMP3Tools
from GuiTools import VWidget

class BottomFrame(QFrame):

    def __init__(self, parent=None):
        """Top Frame of the application. 
        Provides the set of times that handles the preferences of conversion and output"""
        super().__init__(parent)
        self.setStyleSheet("QFrame#bottomFrame {border-top: 1px solid #ADADAD; background-color: #EEEEEE;}")
        self.setObjectName("bottomFrame")
        self.setFixedHeight(160)
        self.initComponents()

        self.layout = QHBoxLayout(self)
        self.setFormatLayout()

        self.layout.addStretch()

        #self.makeConnections()

    def initComponents(self):
        self.formatList = [".mp3 | MPEG Layer 3", ".m4a | AAC Audio Advanced Codec", ".aac | Audio Advanced Codec (raw ADTS)"]
        self.mp3tools = EncoderMP3Tools()
        self.mp2tools = EncoderMP3Tools()
        
    def setFormatLayout(self):
        self.preferencesLayout = VWidget()
        self.layout.addWidget(self.preferencesLayout)

        self.formatBox = QComboBox()
        self.formatBox.addItems(self.formatList)
        self.preferencesLayout.addWidget(self.formatBox)
        self.preferencesLayout.addWidget(self.mp3tools.preferencesWidget)

        #self.setStackedPreferencesLayout()

        self.preferencesLayout.addStretch()

    def setStackedPreferencesLayout(self):
        self.stackedWidget = QStackedWidget()
        self.stackedWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        self.preferencesLayout.addWidget(self.stackedWidget)

        """self.stackedWidget.addWidget(self.mp3tools.preferencesWidget)
        self.stackedWidget.addWidget(self.mp2tools.preferencesWidget)"""

    def makeConnections(self):
        self.formatBox.currentIndexChanged.connect(self.stackedPreferencesLayout.setCurrentIndex)
