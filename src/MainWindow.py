from PySide.QtGui import QWidget, QVBoxLayout, QMainWindow, QStatusBar, QHBoxLayout, \
QFileDialog, QProgressDialog
from PySide.QtCore import QProcess, Qt
from TopFrame import TopFrame
from MetadataFrame import MetadataFrame
from FileListTable import FileListTable, FileListModel
from BottomFrame import BottomFrame
from FileMP3 import FileMP3
from FileAAC import FileAAC
from FileFLAC import FileFLAC
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
        self.metadataFrame = MetadataFrame()
        self.centralWidgetLayout.addWidget(self.metadataFrame)
        
        #Top frame
        self.topFrame = TopFrame()
        self.leftLayout.addWidget(self.topFrame)
        
        #File List Table
        self.fileListTable = FileListTable(self.fileList)
        self.leftLayout.addWidget(self.fileListTable)

        #Bottom Frame
        self.bottomFrame = BottomFrame()
        self.leftLayout.addWidget(self.bottomFrame)

    def makeConections(self):
        """Makes the connections between the signals and slots of the application components."""
        self.topFrame.addFileButton.clicked.connect(self.addFiles)
        self.fileListTable.selectionHasChanged.connect(self.metadataFrame.setFieldValues)

    def updateModel(self):
        indexes = self.fileListSelectionModel.selectedIndexes()
        self.fileListModel.dataChanged.emit(indexes[0], indexes[len(indexes)-1])

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
        elif FileFLAC.isFormatSupported(metaInfo):
            self.fileList.append(FileFLAC(metaInfo))
        else:
            return False
        self.fileListTable.insertRow()

        return True

    def addFolder(self):
        paths = QFileDialog.getExistingDirectory(self, "Add Directory", os.getcwd())
        print(paths)
