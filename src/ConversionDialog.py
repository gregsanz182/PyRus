import threading
from PySide.QtGui import QDialog, QDesktopWidget, QProgressBar, QVBoxLayout, QTableWidget
from GuiTools import CustomCounterWidget

class ConversionDialog(QDialog):

    def __init__(self):
        super().__init__()
        center = QDesktopWidget().availableGeometry().center()
        self.setGeometry(center.x()-300, center.y()-325, 600, 650)
        self.setWindowTitle("Converting Files")
        self.lock = threading.Lock()
        self.initComponents()

    def initComponents(self):
        self.layout = QVBoxLayout(self)

        self.tableList = QTableWidget()
        self.layout.addWidget(self.tableList)

        self.numThreadsWidget = CustomCounterWidget(1, 1, 8)
        self.layout.addWidget(self.numThreadsWidget)

        self.totalProgressBar = QProgressBar()
        self.layout.addWidget(self.totalProgressBar)
        self.totalProgressBar.setMinimum(0)

    def setTotalProgressBarMaximum(self, value: int):
        with self.lock:
            self.totalProgressBar.setMaximum(value)

    def setTotalProgressBarValue(self, value: int):
        with self.lock:
            self.totalProgressBar.setValue(value)
