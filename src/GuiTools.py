from PySide.QtGui import QWidget, QHBoxLayout, QStackedLayout, QVBoxLayout

class HWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def addWidget(self, widget):
        self.layout.addWidget(widget)

    def addLayout(self, layout):
        self.layout.addLayout(layout)
    
    def addStretch(self):
        self.layout.addStretch()

class VWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def addWidget(self, widget):
        self.layout.addWidget(widget)

    def addLayout(self, layout):
        self.layout.addLayout(layout)
    
    def addStretch(self):
        self.layout.addStretch()