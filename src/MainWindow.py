import sys, os
from PySide.QtGui import *
from PySide.QtCore import *
from FileAudio import FileAudio
from FileMP3 import *
from FileListModel import *
from MetadataWidget import *

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.fileList = []
        self.setWindowTitle("PyRus")
        self.setMinimumWidth(1280)
        self.setMinimumHeight(720)

        self.createStatusBar()
        self.createCentralWidget()
        self.pro = QProcess()
        

    def createStatusBar(self):
        """Function to create the Status Bar"""
        self.stBar = QStatusBar()
        self.stBar.showMessage('Ready')
        self.setStatusBar(self.stBar)
        self.stBar.setStyleSheet("QStatusBar { border-top: 1px solid #ADADAD; color: #333333; background-color: #EEEEEE;}")
        self.stBar.setMinimumHeight(25)

    def createCentralWidget(self):
        """Creates the central Widget of the window and all of its components"""

        #Central Widget
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidgetLayout = QGridLayout()
        self.centralWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.centralWidgetLayout.setSpacing(0)
        
        #Top frame
        self.createTopFrame()

        #Central panel
        self.centerLayout = QGridLayout()
        self.centerLayout.setContentsMargins(0, 0, 0, 0)
        self.centerLayout.setSpacing(0)
        
        #Left Panel
        self.centerLeftLayout = QGridLayout()
        self.centerLayout.addLayout(self.centerLeftLayout, 0, 0)
        
        self.createFileListTable()

        self.acceptPanel = QFrame()
        self.acceptPanel.setStyleSheet("QFrame { border-top: 1px solid #ADADAD; background-color: #EEEEEE;}")
        self.acceptPanel.setMaximumHeight(65)
        self.centerLeftLayout.addWidget(self.acceptPanel, 1, 0)
        self.acceptPanelLayout = QGridLayout(self.acceptPanel)
        self.acceptPanelLayout.setContentsMargins(13, 0, 10, 0)

        
        self.startButton = QToolButton()
        self.startButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.startButton.setText("Start")
        self.startButton.setMinimumHeight(57)
        self.startButton.setStyleSheet("QToolButton {padding-left: 13px; padding-right: 13px;}")
        self.startButton.setIcon(QIcon("resources//imgs//startConvert.png"))
        self.startButton.setIconSize(QSize(59, 29))
        self.acceptPanelLayout.addWidget(self.startButton, 0, 3)

        self.acceptPanelLayout.addWidget(QWidget(), 0, 0)
    
        #Metadata panel
        self.createMetadataFrame()
        self.centralWidgetLayout.addLayout(self.centerLayout, 1, 0)

        
        self.centralWidget.setLayout(self.centralWidgetLayout)

    def createTopFrame(self):
        """Creates de Top Frame and all of its components"""
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet("QFrame { border-bottom: 1px solid #ADADAD; background-color: #EEEEEE;}")
        self.topFrame.setMaximumHeight(35)
        self.centralWidgetLayout.addWidget(self.topFrame, 0, 0)
        self.topFrameLayout = QHBoxLayout(self.topFrame)
        self.topFrameLayout.setContentsMargins(5, 3, 5, 3)

        self.addFileButton = QToolButton()
        self.addFileButton.setText("Add file...")
        self.addFileButton.setIcon(QIcon("resources//imgs//addFileIcon.png"))
        self.addFileButton.setMinimumHeight(27)
        self.addFileButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.topFrameLayout.addWidget(self.addFileButton)
        self.addFileButton.clicked.connect(self.addFiles)

        self.addFolderButton = QToolButton()
        self.addFolderButton.setText("Add folder...")
        self.addFolderButton.setIcon(QIcon("resources//imgs//addFolderIcon.png"))
        self.addFolderButton.setMinimumHeight(27)
        self.addFolderButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.topFrameLayout.addWidget(self.addFolderButton)
        self.addFolderButton.clicked.connect(self.addFolder)

        self.optionFormatLayout = QHBoxLayout()
        self.optionFormatLayout.setAlignment(Qt.AlignRight)

        self.formatListBox = QComboBox()
        self.formatListBox.setMinimumHeight(27)
        self.formatListBox.addItem(".mp3")
        self.formatListBox.addItem(".m4a")
        self.formatListBox.addItem(".flac")

        self.optionFormatLayout.addWidget(self.formatListBox)

        self.topFrameLayout.addLayout(self.optionFormatLayout)

    def createMetadataFrame(self):
        self.metadataWidget = MetadataWidget()
        self.centerLayout.addWidget(self.metadataWidget, 0, 1)

    def createFileListTable(self):
        self.fileListTable = QTableView()
        self.fileListModel = FileListModel(self.fileList)
        self.fileListTable.setModel(self.fileListModel)
        self.fileListTable.verticalHeader().setDefaultSectionSize(20)
        self.fileListTable.setStyleSheet("QTableView {border: 0px;}")
        self.fileListTable.horizontalHeader().setMovable(True)
        self.fileListTable.horizontalHeader().setHighlightSections(False)
        self.fileListTable.setColumnWidth(1, 50)
        self.fileListTable.setShowGrid(False)
        self.fileListTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.fileListSelectionModel = self.fileListTable.selectionModel()
        self.fileListSelectionModel.selectionChanged.connect(self.hola)
        self.centerLeftLayout.addWidget(self.fileListTable, 0, 0)

    def hola(self, selected, deselected):
        indexes = self.fileListSelectionModel.selectedRows()
        self.metadataWidget.setFieldValues(self.fileList, indexes)

    def addFiles(self):
        paths = QFileDialog.getOpenFileNames(self, "Add files", os.getcwd())
        progressDialog = QProgressDialog("Adding files", "Cancel", 0, len(paths[0]), self)
        progressDialog.setWindowTitle("Analizing files...")
        progressDialog.setFixedWidth(400)
        progressDialog.setWindowModality(Qt.WindowModal)
        for i, pat in enumerate(paths[0]):
            progressDialog.setLabelText(str(os.path.basename(pat)))
            self.analyseAndAdd(pat)
            progressDialog.setValue(i+1)

    def analyseAndAdd(self, pathFile):
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
            self.fileListTable.model().insertRow(0)
            return True

        return False

    def addFolder(self):
        paths = QFileDialog.getExistingDirectory(self, "Add Directory", os.getcwd())
        print(paths)
