import threading
from PySide.QtGui import QDialog, QDesktopWidget, QProgressBar, QVBoxLayout, QTableWidget, QLabel
from PySide.QtCore import Qt, Signal
from GuiTools import CustomCounterWidget, ConversionTaskBar
from Tools import ProgressObject

class ConversionDialog(QDialog):
    """Dialog that shows the progress of the conversion tasks and
    provides items that allow tasks manipulation"""

    #This signal is emited to connect the thread with its corresponing progress bar
    connectBarSignal = Signal(Signal, str)

    def __init__(self):
        """Constructor of the class"""
        super().__init__()
        #Centers the dialog in the middle of the screen
        center = QDesktopWidget().availableGeometry().center()
        self.setGeometry(center.x()-300, center.y()-325, 600, 650)

        self.setWindowTitle("Converting Files")

        #This lock allows the sinchronization of the threads when
        #they need to modify the common widgets
        self.lock = threading.Lock()

        self.initComponents()
        self.makeConections()

        #List of progress bar of each task
        #Every bar is recycled when the threads finish their tasks
        self.bars = list()

    def initComponents(self):
        """Initializes the components of the Dialog"""
        self.layout = QVBoxLayout(self)

        #Layout that contains all the individual progress bars
        self.barsLayout = QVBoxLayout()
        self.barsLayout.setAlignment(Qt.AlignTop)
        self.barsLayout.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(self.barsLayout)

        self.tableList = QTableWidget()
        self.layout.addWidget(self.tableList)

        self.numThreadsWidget = CustomCounterWidget("Number of Converters:", 1, 1, 5)
        self.layout.addWidget(self.numThreadsWidget)

        self.totalProgressBar = QProgressBar()
        self.layout.addWidget(self.totalProgressBar)
        self.totalProgressBar.setMinimum(0)

    def makeConections(self):
        """Makes the connection of the signals with thier corresponding slots"""
        self.connectBarSignal.connect(self.connectTaskSlot)

    def setTotalProgressBarMaximum(self, value: int):
        """Sets the maximum value of the global progress bar"""
        with self.lock:
            self.totalProgressBar.setMaximum(value)

    def setTotalProgressBarValue(self, value: int):
        """Sets the value of the global progress bar"""
        self.totalProgressBar.setValue(value)

    def setTotalProgressBarIncrementedValue(self, incrementedValue: int):
        """Incremets the value of the global progress bar to the amount passed as argument"""
        self.totalProgressBar.setValue(incrementedValue + self.totalProgressBar.value())

    def connectTaskSlot(self, signal: Signal, labelText: str):
        """Connects the thread update signal to its correponding progress bar, as well as
        the global progress bar"""
        bar = None

        #Seraches if there is an already iniialized idle visible bar
        for itemBar in self.bars:
            if itemBar.isBusy() is False and itemBar.isVisible():
                bar = itemBar
                break

        #If no bar is found, searches for an already initialized idle hidden bar 
        if bar is None:
            for itemBar in self.bars:
                if itemBar.isBusy() is False:
                    bar = itemBar
                    break

        #If no bar is found, initializes a bar and appends it to the list
        if bar is None:
            bar = ConversionTaskBar()
            self.barsLayout.addWidget(bar)
            self.bars.append(bar)

        #Resets the bar to its initial values
        bar.resetBar(labelText)
        bar.makeConection(signal)
        bar.setVisible(True)
        signal.connect(self.updateGlobalStatus)

    def updateGlobalStatus(self, progress: ProgressObject, threadNumber: int):
        """Slot that updates the global status"""
        with self.lock:
            self.setTotalProgressBarIncrementedValue(progress.incrementedProgress)

    def connectTask(self, signal: Signal, labelText: str):
        """Emits the signal that triggers and allows the creation and connection of the bar
        to its corresponding thread"""
        self.connectBarSignal.emit(signal, labelText)

    def hideIdleBars(self, amount: int):
        """Hide the bars that are not busy and visible.
        Handful when there are more visible bars then running threads.
        The argument amount specifies the quantity of bars to hide"""
        for bar in self.bars:
            if amount > 0:
                if bar.isBusy() is False and bar.isVisible():
                    bar.setVisible(False)
                    amount -= 1
            else:
                break

    def visibleBars(self) -> int:
        """Returns the total of visible bars at the moment of its call"""
        return sum(1 for bar in self.bars if bar.isVisible() is True)
