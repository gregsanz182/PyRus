from PySide.QtGui import QFrame, QHBoxLayout, QToolButton, QIcon
from PySide.QtCore import Qt

class TopFrame(QFrame):
    """Top Frame of the application. Provides add and delete buttons for file list managing"""

    def __init__(self, parent=None):
        """Constructor of the class. Initializes and sets all the components"""
        super().__init__(parent)
        self.setStyleSheet("QFrame#topFrame {border-bottom: 1px solid #ADADAD; background-color: #EEEEEE;}")
        self.setObjectName("topFrame")
        self.setFixedHeight(35)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(7, 0, 7, 0)

        self.addFileButton = ToolButton("Add file...", QIcon("resources/imgs/addFileIcon.png"))
        self.layout.addWidget(self.addFileButton, alignment=Qt.AlignVCenter)

        self.addFolderButton = ToolButton("Add folder...", QIcon("resources/imgs/addFolderIcon.png"))
        self.layout.addWidget(self.addFolderButton, alignment=Qt.AlignVCenter)

        self.addSeparator()

        self.removeFileButton = ToolButton("Remove", QIcon("resources/imgs/removeFileIcon2.png"))
        self.layout.addWidget(self.removeFileButton, alignment=Qt.AlignVCenter)

        self.clearListButton = ToolButton("Clear List", QIcon("resources/imgs/removeAllIcon.png"))
        self.layout.addWidget(self.clearListButton, alignment=Qt.AlignVCenter)

        self.layout.addStretch()

        self.selectAllButton = ToolButton("Select All", QIcon("resources/imgs/selectAllIcon.png"))
        self.layout.addWidget(self.selectAllButton, alignment=Qt.AlignVCenter)


    def addSeparator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet("QFrame#TopFrameSeparator {color: #ADADAD;}")
        separator.setObjectName("TopFrameSeparator")
        separator.setFixedHeight(25)
        self.layout.addSpacing(3)
        self.layout.addWidget(separator, alignment=Qt.AlignVCenter)
        self.layout.addSpacing(3)


class ToolButton(QToolButton):
    """Common Tool Button used in the top frame for file managing of the list"""

    def __init__(self, text="", icon=QIcon(), parent=None):
        """Constructor of the class. Initializes and sets all the components"""
        super().__init__(parent)
        self.setText(text)
        self.setIcon(icon)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setFixedHeight(27)
