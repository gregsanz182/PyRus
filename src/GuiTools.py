from PySide.QtGui import QWidget, QHBoxLayout, QStackedLayout, QVBoxLayout, QComboBox, \
QSizePolicy, QStyledItemDelegate, QCheckBox, QFormLayout, QLineEdit, QToolButton, QFrame, QLabel, \
QToolButton, QProgressBar
from PySide.QtCore import Qt, Signal, QSize

class CustomHFormLayout(QHBoxLayout):
    """Custom QHBoxLayout that behaves like a QFormLayout. Arranges every item like a form, but with label above the text field.
    Extends QHBoxLayout"""

    def __init__(self, parent=None):
        """Constructor of the class. Initializes and sets all the components"""
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setAlignment(Qt.AlignLeft)

    def addField(self, label=None, widgetField=None):
        """Adds the given label and widget in the layout"""
        vlayout = QVBoxLayout()
        vlayout.setSpacing(2)
        self.addLayout(vlayout)
        vlayout.addWidget(label)
        vlayout.addWidget(widgetField)
        vlayout.addStretch()
        self.addSpacing(5)

    def addSeparator(self):
        """Adds a separator to the layout"""
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.addSpacing(5)
        self.addWidget(separator)
        self.addSpacing(5)

    def setContentsMargin(self, margin: int):
        self.setContentsMargins(margin, margin, margin, margin)

class CustomVFormLayout(QVBoxLayout):
    """Custom QVBoxLayout that behaves like a QFormLayout. Arranges every item like a form, but with label above the text field.
    Extends QVBoxLayout"""

    def __init__(self, parent=None):
        """Constructor of the class. Initializes and sets all the components"""
        super().__init__(parent)
        self.setSpacing(2)

    def addField(self, label: QLabel=None, widgetField: QWidget=None):
        """Adds the given label and widget in the layout"""
        self.addWidget(label)
        self.addWidget(widgetField)
        self.addSpacing(5)

    def addSeparator(self):
        """Adds a separator to the layout"""
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.addSpacing(5)
        self.addWidget(separator)
        self.addSpacing(5)
    
    def setContentsMargin(self, margin: int):
        self.setContentsMargins(margin, margin, margin, margin)

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

class CustomComboBox(QComboBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        #self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setItemDelegate(QStyledItemDelegate())
        self.setFixedHeight(23)

    def setHorizontalSizePolicy(self, horizontalPolicy):
        self.setSizePolicy(horizontalPolicy, self.sizePolicy().verticalPolicy())


class CheckFormWidget(QWidget):

    def __init__(self, leftWidget, rightWidget=None, text="", parent=None):
        super().__init__(parent)
        self.setMaximumWidth(400)
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

        self.makeConnections()
        self.changeState(Qt.Unchecked)

    def makeConnections(self):
        self.checkBox.stateChanged.connect(self.changeState)

    def changeState(self, state):
        if state == Qt.Checked:
            self.leftWidget.setEnabled(True)
            self.rightWidget.setEnabled(True)
        else:
            self.leftWidget.setEnabled(False)
            self.rightWidget.setEnabled(False)

    def getState(self):
        return self.checkBox.checkState()

class CustomCounterWidget(QWidget):

    counterChanged = Signal(int)

    def __init__(self, text="", initValue=1, minimum=None, maximum=None, parent=None):
        super().__init__(parent)
        self.actualValue = initValue
        self.minimum = minimum
        self.maximum = maximum
        self.labelText = QLabel(text)
        self.initComponents()
        self.makeConnections()

    def initComponents(self):
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignLeft)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.labelText)

        self.lessButton = QToolButton()
        self.lessButton.setFixedSize(QSize(22, 22))
        self.lessButton.setText("-")
        self.layout.addWidget(self.lessButton)

        self.numLineEdit = QLineEdit(str(self.actualValue))
        self.numLineEdit.setFixedWidth(30)
        self.numLineEdit.setReadOnly(True)
        self.layout.addWidget(self.numLineEdit)

        self.moreButton = QToolButton()
        self.moreButton.setFixedSize(QSize(22, 22))
        self.moreButton.setText("+")
        self.layout.addWidget(self.moreButton)

        self.layout.addStretch()

    def makeConnections(self):
        self.lessButton.clicked.connect(self.decreaseValue)
        self.moreButton.clicked.connect(self.increaseValue)

    def increaseValue(self):
        if self.maximum is None or (self.actualValue + 1) <= self.maximum:
            self.actualValue += 1
            self.numLineEdit.setText(str(self.actualValue))
            self.counterChanged.emit(self.actualValue)

    def decreaseValue(self):
        if self.minimum is None or (self.actualValue - 1) >= self.minimum:
            self.actualValue -= 1
            self.numLineEdit.setText(str(self.actualValue))
            self.counterChanged.emit(self.actualValue)

class ConversionTaskBar(QWidget):

    def __init__(self):
        super().__init__()
        self.busy = False
        self.initComponents()

    def initComponents(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.label = QLabel()
        self.layout.addWidget(self.label)

        self.progressBar = QProgressBar()
        self.progressBar.setMaximum(100)
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(0)
        self.progressBar.setFixedHeight(8)
        self.layout.addWidget(self.progressBar)

    def updateProgress(self, progressIncreased: int, dh, sj):
        self.progressBar.setValue(self.progressBar.value() + progressIncreased)
        if self.progressBar.value() >= self.progressBar.maximum():
            self.busy = False

    def resetBar(self, labelText=''):
        self.changeLabel(labelText)
        self.progressBar.setValue(0)
        self.busy = True

    def changeLabel(self, string: str):
        self.label.setText(string)

    def isBusy(self) -> bool:
        return self.busy

    def makeConection(self, signal):
        signal.connect(self.updateProgress)
