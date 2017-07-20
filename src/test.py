from PySide.QtCore import *
from PySide.QtGui import *
import base64
import sys

class MyModel(QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self.items = 0
        self.header = ["Head 1", "Head 2", "Head 3"]
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timerHit)
        self.timer.start()

    def timerHit(self):
        topLeft = self.createIndex(2, 1)
        self.insertRow(0)
        #self.dataChanged.emit(topLeft, topLeft)

    def rowCount(self, parent):
        return 5

    def columnCount(self, parent):
        return 10

    def data(self, index, role):
        if index.row() == 2 and index.column() == 1 and role == Qt.DisplayRole:
            return QTime.currentTime()
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            for i in range(10):
                if section == i:
                    return "Header " + str(i)

        return None

    def insertRows(self, row, count, parent):
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        self.endInsertRows()
        return True

if __name__ == "__main__":
    try:
        mainApp = QApplication(sys.argv)

        myModel = MyModel()
        
        mainWindow = QTableView()
        mainWindow.setModel(myModel)
        mainWindow.verticalHeader().setDefaultSectionSize(20)
        mainWindow.horizontalHeader().setMovable(True)
        mainWindow.setWindowTitle("Table test")
        mainWindow.setGeometry(640, 480, 500, 500)
        mainWindow.show()

        mainApp.exec_()
        sys.exit(0)
    except NameError:
        print("Name error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing window...")
    except Exception:
        print(sys.exc_info()[1])

