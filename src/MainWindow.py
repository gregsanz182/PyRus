from PySide.QtGui import QWidget, QVBoxLayout, QMainWindow, QStatusBar, QHBoxLayout, \
QFileDialog, QProgressDialog
from PySide.QtCore import QProcess, Qt
from TopFrame import TopFrame
from MetadataWidget import MetadataWidget
from FileListTable import FileListTable, FileListModel
from BottomFrame import BottomFrame
from FileMP3 import FileMP3
from FileAAC import FileAAC
import os

class MainWindow(QMainWindow):
    """Main Windows of the Application"""

    def __init__(self):
        """Constructor of the class. Sets all the settings and initializes all the components"""
        super().__init__()
        self.fileList = []
        self.setWindowTitle("PyRus")

        #Minimun size of the Window
        self.setMinimumWidth(1280)
        self.setMinimumHeight(720)

        self.createStatusBar()
        self.createCentralWidget()
        self.makeConections()

        self.pro = QProcess()
        

    def createStatusBar(self):
        """Creates and sets the Status Bar of the Window"""
        self.stBar = QStatusBar()
        self.stBar.showMessage('Ready')
        self.setStatusBar(self.stBar)
        self.stBar.setStyleSheet("QStatusBar#statusbar {border-top: 1px solid #ADADAD; color: #333333; background-color: #EEEEEE;}")
        self.stBar.setObjectName("statusbar")
        self.stBar.setMinimumHeight(25)

    def createCentralWidget(self):
        """Creates the central Widget of the window and all of its components"""
        #Central Widget
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        #Layout of the Central Widget
        self.centralWidgetLayout = QHBoxLayout(self.centralWidget)
        self.centralWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.centralWidgetLayout.setSpacing(0)

        #Layout of the left side of the Central Widget
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.centralWidgetLayout.addLayout(self.leftLayout)

        #MetadataFrame or right side of  the Central Widget
        self.metadataWidget = MetadataWidget()
        self.centralWidgetLayout.addWidget(self.metadataWidget)
        
        #Top frame
        self.topFrame = TopFrame()
        self.leftLayout.addWidget(self.topFrame)
        
        #File List Table
        self.fileListTable = FileListTable()
        self.fileListTable.setModel(FileListModel(self.fileList))
        self.leftLayout.addWidget(self.fileListTable)

        #Bottom Frame
        self.bottomFrame = BottomFrame()
        self.leftLayout.addWidget(self.bottomFrame)

        
        """
        #Central panel
        self.centerLayout = QGridLayout()
        self.centerLayout.setContentsMargins(0, 0, 0, 0)
        self.centerLayout.setSpacing(0)
        
        #Left Panel
        self.centerLeftLayout = QGridLayout()
        self.centerLayout.addLayout(self.centerLeftLayout, 0, 0)
        
        self.createFileListTable()

        self.acceptPanel = QFrame()
        self.acceptPanel.setStyleSheet("QFrame#acceptPanel {border-top: 1px solid #ADADAD; background-color: #EEEEEE;}")
        self.acceptPanel.setObjectName("acceptPanel")
        self.acceptPanel.setMaximumHeight(65)
        self.centerLeftLayout.addWidget(self.acceptPanel, 1, 0)
        self.acceptPanelLayout = QGridLayout(self.acceptPanel)
        self.acceptPanelLayout.setContentsMargins(13, 0, 10, 0)

        
        self.startButton = QToolButton()
        self.startButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.startButton.setText("Start")
        self.startButton.setMinimumHeight(57)
        self.startButton.setStyleSheet("QToolButton#startButton {padding-left: 13px; padding-right: 13px;}")
        self.startButton.setObjectName("startButton")
        self.startButton.setIcon(QIcon("resources//imgs//startConvert.png"))
        self.startButton.setIconSize(QSize(59, 29))
        self.acceptPanelLayout.addWidget(self.startButton, 0, 3)

        self.acceptPanelLayout.addWidget(QWidget(), 0, 0)
    
        #Metadata panel
        self.createMetadataFrame()
        self.centralWidgetLayout.addLayout(self.centerLayout, 1, 0)

        
        self.centralWidget.setLayout(self.centralWidgetLayout)"""

    def makeConections(self):
        """Makes the connections between the signals and slots of the application components."""
        self.topFrame.addFileButton.clicked.connect(self.addFiles)

    def updateModel(self):
        indexes = self.fileListSelectionModel.selectedIndexes()
        self.fileListModel.dataChanged.emit(indexes[0], indexes[len(indexes)-1])

    def createFileListTable(self):
        self.fileListTable = QTableView()
        self.fileListModel = FileListModel(self.fileList)
        self.fileListTable.setModel(self.fileListModel)
        self.fileListTable.verticalHeader().setDefaultSectionSize(20)
        self.fileListTable.setStyleSheet("QTableView#fileListTable {border: 0px;}")
        self.fileListTable.setObjectName("fileListTable")
        self.fileListTable.horizontalHeader().setMovable(True)
        self.fileListTable.horizontalHeader().setHighlightSections(False)
        self.fileListTable.setColumnWidth(1, 50)
        self.fileListTable.setShowGrid(False)
        self.fileListTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.fileListSelectionModel = self.fileListTable.selectionModel()
        self.fileListSelectionModel.selectionChanged.connect(self.changeMetadataWidgetValues)
        self.centerLeftLayout.addWidget(self.fileListTable, 0, 0)

    def changeMetadataWidgetValues(self, selected, deselected):
        indexes = self.fileListSelectionModel.selectedRows()
        self.metadataWidget.setFieldValues(self.fileList, indexes)

    def addFiles(self):
        """Opens a QFileDialog and imports the selected files.
        Provides a QProgressDialog that shows the progress of the operation.
        Every file is sent to a method that analyse the file, and if it is
        supported, it's being addded to the file list of the application. If it's not,
        then it's ignored"""
        paths = QFileDialog.getOpenFileNames(self, "Add files", os.getcwd())
        if len(paths[0]) > 0:
            progressDialog = QProgressDialog("Adding files", "Cancel", 0, len(paths[0]), self)
            progressDialog.setWindowTitle("Analizing files...")
            progressDialog.setFixedWidth(400)
            progressDialog.setWindowModality(Qt.WindowModal)
            progressDialog.show()
            for i, pat in enumerate(paths[0]):
                progressDialog.setLabelText(str(os.path.basename(pat)))
                self.analyseAndAdd(pat)
                progressDialog.setValue(i+1)
            progressDialog.close()

    def analyseAndAdd(self, pathFile):
        """Analyzes the file in the pathFile with mediainfo CLI. This method selects the
        appropriate format, adds the file to the list and returns True. if the file is not supported, then
        returns False."""
        metaInfo = {}
        process = QProcess()
        process.start("resources/tools/mediainfo.exe", [pathFile])
        process.waitForFinished()
        infoType = ''
        while process.canReadLine():
            cad = str(process.readLine()).split(": ", 1)
            if len(cad) == 2:
                metaInfo[infoType].update({cad[0].rstrip(): cad[1].rstrip('\r\n')})
            elif len(cad[0].rstrip('\r\n').rstrip()) > 0:
                infoType = cad[0].rstrip('\r\n').rstrip()
                metaInfo[infoType] = {}

        if FileMP3.isFormatSupported(metaInfo):
            self.fileList.append(FileMP3(metaInfo))
        elif FileAAC.isFormatSupported(metaInfo):
            self.fileList.append(FileAAC(metaInfo))
        else:
            return False
        self.fileListTable.model().insertRow(0)

        return True

    def addFolder(self):
        paths = QFileDialog.getExistingDirectory(self, "Add Directory", os.getcwd())
        print(paths)
