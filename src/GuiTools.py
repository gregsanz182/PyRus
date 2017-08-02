from PySide.QtGui import QWidget, QHBoxLayout, QStackedLayout, QVBoxLayout, QComboBox, \
QSizePolicy, QStyledItemDelegate, QCheckBox, QFormLayout, QLineEdit, QToolButton
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

class WidgetList():

    def __init__(self):
        self.list = []

    def appendWidget(self, widget: QWidget):
        self.list.append(widget)

    def showOnlyAWidget(self, index: int):
        for i, widget in enumerate(self.list):
            if i == index:
                widget.setVisible(True)
            else:
                widget.setVisible(False)

    def showWidget(self, index: int):
        if index >= 0 and index < len(self.list):
            self.list[index].setVisible(True)

    def hideWidget(self, index: int):
        if index >= 0 and index < len(self.list):
            self.list[index].setVisible(False)


class SwitchingWidget(QWidget):

    def __init__(self, orientation=Qt.Horizontal, parent=None):
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


class CheckFormWidget(QWidget):

    def __init__(self, leftWidget, rightWidget=None, text="", parent=None):
        super().__init__(parent)
        self.setMaximumWidth(350)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(1)
        self.checkBox = QCheckBox(text)
        self.layout.addWidget(self.checkBox)
        
        self.bottomLayout = QHBoxLayout()
        self.layout.addLayout(self.bottomLayout)
        self.leftWidget = leftWidget
        self.bottomLayout.addWidget(self.leftWidget)
        if rightWidget is not None:
            self.rightWidget = rightWidget
            self.bottomLayout.addWidget(self.rightWidget)

        self.makeConections()
        self.changeState(Qt.Unchecked)

    def makeConections(self):
        self.checkBox.stateChanged.connect(self.changeState)

    def changeState(self, state):
        if state == Qt.Checked:
            self.leftWidget.setEnabled(True)
            self.rightWidget.setEnabled(True)
        else:
            self.leftWidget.setEnabled(False)
            self.rightWidget.setEnabled(False)
