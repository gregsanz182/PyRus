from PySide.QtGui import QTableView, QAbstractItemView, QBrush, QColor
from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex, Signal

class FileListTable(QTableView):
    """Table that contains the List of Files to convert. Provides information and details about the files in the list"""

    selectionHasChanged = Signal(list, list)

    def __init__(self, fileList=list(), parent=None):
        """Constructor of the class. Initializes and sets all the components.
        Recieves the list of files."""
        super().__init__(parent)
        self.fileList = fileList
        self.verticalHeader().setDefaultSectionSize(20)
        self.setStyleSheet("QTableView#fileListTable {border: 0px;}")
        self.setObjectName("fileListTable")
        self.horizontalHeader().setMovable(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setShowGrid(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setModel(FileListModel(self.fileList))
        self.modelSelection = self.selectionModel()
        self.modelSelection.selectionChanged.connect(self.selectionChangedHandle)

    def selectionChangedHandle(self):
        """Handles the 'selectionChanged' emited signal and emits 
        selectionHasChanged signal with fileList and the index 
        of selected the items"""
        indexes = self.modelSelection.selectedRows()
        self.selectionHasChanged.emit(indexes, self.fileList)

    def insertRow(self):
        """Inserts a single row"""
        self.model().insertSingleRow()


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

    def rowCount(self, parent=QModelIndex()):
        """Overrides the parent method. Returns the total rows of the model"""
        return len(self.list)

    def columnCount(self, parent=QModelIndex()):
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
        Returns the data for the given role and section in the header
        with the specified orientation."""
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self.header[section]
            if role == Qt.TextAlignmentRole:
                return Qt.AlignLeft

        return None

    def insertSingleRow(self):
        """Inserts a single row to the model."""
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.endInsertRows()
        return True
    