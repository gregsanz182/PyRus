from PySide.QtGui import QFrame, QHBoxLayout, QToolButton, QIcon
from PySide.QtCore import Qt

class TopFrame(QFrame):
    """Top Frame of the application. Provides add and delete buttons for file list managing"""

    def __init__(self, parent=None):
        """Constructor of the class. Initializes and sets all of the components"""
        super().__init__(parent)
        self.setStyleSheet("QFrame#topFrame {border-bottom: 1px solid #ADADAD; background-color: #EEEEEE;}")
        self.setObjectName("topFrame")
        self.setFixedHeight(35)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 0, 5, 0)

        self.addFileButton = QToolButton()
        self.addFileButton.setText("Add file...")
        self.addFileButton.setIcon(QIcon("resources/imgs/addFileIcon.png"))
        self.addFileButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addFileButton.setFixedHeight(27)
        self.layout.addWidget(self.addFileButton, alignment=Qt.AlignVCenter)

        self.addFileButton = QToolButton()
        self.addFileButton.setText("Add folder...")
        self.addFileButton.setIcon(QIcon("resources/imgs/addFolderIcon.png"))
        self.addFileButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addFileButton.setFixedHeight(27)
        self.layout.addWidget(self.addFileButton, alignment=Qt.AlignVCenter)
        
        self.layout.addStretch()

