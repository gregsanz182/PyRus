from PySide.QtGui import *
from PySide.QtCore import *

class FileListModel(QAbstractTableModel):

    def __init__(self, fileList):
        super().__init__()
        self.list = fileList
        self.header = ["Filename", "#", "Artist", "Title", "Album", "Album Artist", "Year", "Genre", "Lenght"]
        self.fields = ["<filename>", "<tracknumber>", "<artist>", "<title>", "<album>", "<albumartist>", "<year>", "<genre>", "<lenght>"]

    def rowCount(self, parent):
        return len(self.list)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.list[index.row()].metadata[self.fields[index.column()]]

        if role == Qt.BackgroundRole:
            if index.row()%2 == 0:
                return QBrush(QColor("#F8F8F8"))
            else:
                return QBrush(QColor("#FFFFFF"))

        return None

    def headerData(self, section, orientation, role):
        height = 27
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self.header[section]
            if role == Qt.TextAlignmentRole:
                return Qt.AlignLeft

        return None

    def insertRows(self, row, count, parent):
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        self.endInsertRows()
        return True
    