from PySide.QtGui import *
from PySide.QtCore import *

class FileListModel(QAbstractTableModel):

    def __init__(self, fileList):
        super().__init__()
        self.list = fileList
        self.header = ["Filename", "#", "Artist", "Title", "Album", "Album Artist", "Year", "Genre", "Lenght"]

    def rowCount(self, parent):
        return len(self.list)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self.list[index.row()].filename
            elif index.column() == 1:
                return self.list[index.row()].track
            elif index.column() == 2:
                return self.list[index.row()].artist
            elif index.column() == 3:
                return self.list[index.row()].title
            elif index.column() == 4:
                return self.list[index.row()].album
            elif index.column() == 5:
                return self.list[index.row()].album_artist
            elif index.column() == 6:
                return self.list[index.row()].year
            elif index.column() == 7:
                return self.list[index.row()].genre
            elif index.column() == 8:
                return self.list[index.row()].duration

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
