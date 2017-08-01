from PySide.QtGui import QFrame, QVBoxLayout, QComboBox, QHBoxLayout, QStackedLayout, QStackedWidget, QSizePolicy
from PySide.QtCore import Qt
from EncoderMP3Tools import EncoderMP3Tools
from GuiTools import SwitchingWidget

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
        self.setFormatWidget()

        self.layout.addStretch()

    def initComponents(self):
        self.mp3tools = EncoderMP3Tools()
        self.mp2tools = EncoderMP3Tools()
        
    def setFormatWidget(self):
        self.sw = SwitchingWidget(Qt.Vertical)
        self.layout.addWidget(self.sw)
        self.sw.addItem(self.mp3tools.formatNameByExtensions[".mp3"], self.mp3tools.preferencesWidget)
        self.sw.addItem(".flac | Free Lossless Audio Codec", self.mp2tools.preferencesWidget)
        self.sw.addStretch()