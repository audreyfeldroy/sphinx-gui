from PySide import QtGui, QtCore

from editor import Editor
from preview import Preview


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        treeview =  QtGui.QTreeView()
        self.editor = Editor()
        self.preview = Preview()
        self.setCentralWidget(splitter)
        
        # Small treeview, big editor
        treeview.setMaximumWidth(250)
        
        splitter.addWidget(treeview)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview)

        self.setWindowTitle("RST Previewer")
        self.showMaximized()
        
        self.setupActions()

    def setupActions(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.openAction = QtGui.QAction(
                                QtGui.QIcon(":/images/open.png"), 
                                "&Open", 
                                self, 
                                shortcut="Ctrl+O",
                                statusTip="Open File", 
                                triggered=self.openFile
                            )
        self.fileMenu.addAction(self.openAction)

    def openFile(self, path=None):
        if not path:
            path = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                    '', "ReStructuredText Files (*.rst)")
    
        if path:
            inFile = QtCore.QFile(path[0])
            if inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                text = inFile.readAll()
    
                try:
                    # Python v3.
                    text = str(text, encoding='ascii')
                except TypeError:
                    # Python v2.
                    text = str(text)
    
                self.editor.setPlainText(text)