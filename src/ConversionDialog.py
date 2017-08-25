import threading
from PySide.QtGui import QDialog, QDesktopWidget, QProgressBar, QVBoxLayout, QTableWidget, QFormLayout, QLabel
from PySide.QtCore import Qt, Signal
from GuiTools import CustomCounterWidget, ConversionTaskBar

class ConversionDialog(QDialog):

    connectBarSignal = Signal(Signal, str)

    def __init__(self):
        super().__init__()
        center = QDesktopWidget().availableGeometry().center()
        self.setGeometry(center.x()-300, center.y()-325, 600, 650)
        self.setWindowTitle("Converting Files")
        self.lock = threading.Lock()
        self.initComponents()
        self.makeConections()
        self.bars = list()

    def initComponents(self):
        self.layout = QVBoxLayout(self)

        self.barsLayout = QVBoxLayout()
        self.barsLayout.setAlignment(Qt.AlignTop)
        self.barsLayout.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(self.barsLayout)

        self.tableList = QTableWidget()
        self.layout.addWidget(self.tableList)

        self.numThreadsWidget = CustomCounterWidget("Number of Converters:", 1, 1, 8)
        self.layout.addWidget(self.numThreadsWidget)

        self.totalProgressBar = QProgressBar()
        self.layout.addWidget(self.totalProgressBar)
        self.totalProgressBar.setMinimum(0)

    def makeConections(self):
        self.connectBarSignal.connect(self.connectTaskSlot)

    def setTotalProgressBarMaximum(self, value: int):
        with self.lock:
            self.totalProgressBar.setMaximum(value)

    def setTotalProgressBarValue(self, value: int):
        with self.lock:
            self.totalProgressBar.setValue(value)

    def connectTaskSlot(self, signal, labelText):
        bar = None
        for itemBar in self.bars:
            if itemBar.isBusy() is False and itemBar.isVisible():
                bar = itemBar
                break
        if bar is None:
            for itemBar in self.bars:
                if itemBar.isBusy() is False:
                    bar = itemBar
                    break

        if bar is None:
            bar = ConversionTaskBar()
            self.barsLayout.addWidget(bar)
            self.bars.append(bar)

        bar.resetBar(labelText)
        bar.makeConection(signal)
        bar.setVisible(True)

    def connectTask(self, signal, labelText):
        self.connectBarSignal.emit(signal, labelText)

    def hideIdleBars(self, amount: int):
        for bar in self.bars:
            if amount > 0:
                if bar.isBusy() is False and bar.isVisible():
                    bar.setVisible(False)
                    amount -= 1
            else:
                break

    def visibleBars(self) -> int:
        return sum(1 for bar in self.bars if bar.isVisible() is True)
