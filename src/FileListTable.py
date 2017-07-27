from PySide.QtGui import QTableView, QAbstractItemView, QBrush, QColor
from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex

class FileListTable(QTableView):
    """Table that contains the List of Files to convert. Provides information and details about the files in the list"""

    def __init__(self, parent=None):
        """Constructor of the class. Initializes and sets all the components"""
        super().__init__(parent)
        self.verticalHeader().setDefaultSectionSize(20)
        self.setStyleSheet("QTableView#fileListTable {border: 0px;}")
        self.setObjectName("fileListTable")
        self.horizontalHeader().setMovable(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setShowGrid(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

class FileListModel(QAbstractTableModel):
    """Model that represents the data of the FileListTable"""

    def __init__(self, fileList):
        """Constructor of the class. Initializes and sets all the components"""
        super().__init__()
        self.list = fileList
        self.header = ["Filename", "#", "Artist", "Title", "Album", "Album Artist", "Year", "Genre", "Lenght"]
        self.fields = ["<filename>", "<tracknumber>", "<artist>", "<title>", "<album>", "<albumartist>", "<year>", "<genre>", "<lenght>"]

    def setFileList(self, fileList):
        """Sets the File List for the Model"""
        self.list = fileList

    def rowCount(self, parent):
        """Overrides the parent method. Returns the total rows of the model"""
        return len(self.list)

    def columnCount(self, parent):
        """Overrides the parent method. Returns the total columns of the model"""
        return len(self.header)

    def data(self, index, role):
        """Overrides the parent method. 
        Returns the data stored under the given role for the item referred to by the index."""
        if role == Qt.DisplayRole:
            return self.list[index.row()].metadata[self.fields[index.column()]]

        if role == Qt.BackgroundRole:
            if index.row()%2 == 0:
                return QBrush(QColor("#F8F8F8"))
            else:
                return QBrush(QColor("#FFFFFF"))

        return None

    def headerData(self, section, orientation, role):
        """Overrides the parent method. 
        Returns the data for the given role and section in the header with the specified orientation."""
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self.header[section]
            if role == Qt.TextAlignmentRole:
                return Qt.AlignLeft

        return None

    def insertRows(self, row, count, parent):
        """Overrides the parent method.
        Inserts count rows into the model before the given row."""
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        self.endInsertRows()
        return True
    
