from PySide.QtGui import QWidget, QHBoxLayout, QStackedLayout, QVBoxLayout, QComboBox, QSizePolicy, QStyledItemDelegate
from PySide.QtCore import Qt

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

class SwitchingWidget(QWidget):

    def __init__(self, orientation=Qt.Horizontal, titleLabel="", parent=None):
        super().__init__(parent)
        if orientation == Qt.Horizontal:
            self.layout = QHBoxLayout(self)
        else:
            self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.comboBox = ComboBox()
        self.layout.addWidget(self.comboBox)
        self.widgetList = []
        self.makeConnections()

    def addItem(self, text, widget):
        if len(self.widgetList) == 0:
            widget.setVisible(True)
        else:
            widget.setVisible(False)
        self.comboBox.addItem(text)
        self.widgetList.append(widget)
        self.layout.addWidget(widget)
    
    def addStretch(self):
        self.layout.addStretch()

    def setWidgetVisible(self, index):
        for i, widget in enumerate(self.widgetList):
            if i == index:
                widget.setVisible(True)
            else:
                widget.setVisible(False)

    def makeConnections(self):
        self.comboBox.currentIndexChanged.connect(self.setWidgetVisible)

class ComboBox(QComboBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setItemDelegate(QStyledItemDelegate())
        self.setStyleSheet("QComboBox QAbstractItemView::item { min-height: 15px;}")
        self.setFixedHeight(23)

    def setHorizontalSizePolicy(self, horizontalPolicy):
        self.setSizePolicy(horizontalPolicy, self.sizePolicy().verticalPolicy())
