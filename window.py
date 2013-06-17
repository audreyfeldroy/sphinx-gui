from PySide import QtGui, QtCore
from unipath import Path

from dialogs import OpenDialog
from editor import Editor
from preview import Preview
from tree import Tree


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.tree =  Tree()
        self.editor = Editor()
        self.preview = Preview()
        self.file_path = None
        self.setCentralWidget(splitter)        
        splitter.addWidget(self.tree)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview)

        self.setWindowTitle("RST Previewer")
        self.showMaximized()
        
        self.setupActions()

    def setupActions(self):
        """
            Set up the top menu actions and keyboard shortcuts.
        """
        self.fileMenu = self.menuBar().addMenu("&File")

        self.openAction = QtGui.QAction(
                                QtGui.QIcon(":/images/open.png"), 
                                "&Open File", 
                                self, 
                                shortcut="Ctrl+O",
                                statusTip="Open File", 
                                triggered=self.openFile
                            )
        self.fileMenu.addAction(self.openAction)

        self.openFolderAction = QtGui.QAction(
                                    QtGui.QIcon(":/images/open.png"), 
                                    "Open &Folder", 
                                    self, 
                                    shortcut="Ctrl+F",
                                    statusTip="Open Folder", 
                                    triggered=self.openFolder
                                )
        self.fileMenu.addAction(self.openFolderAction)
        

        self.saveAction = QtGui.QAction(
                                QtGui.QIcon(":/images/save.png"), 
                                "&Save File", 
                                self, 
                                shortcut="Ctrl+S",
                                statusTip="Save File", 
                                triggered=self.saveFile
                            )
        self.fileMenu.addAction(self.saveAction)

        self.saveAsAction = QtGui.QAction(
                                QtGui.QIcon(":/images/save.png"), 
                                "&Save As File", 
                                self, 
                                shortcut="Ctrl+Shift+S",
                                statusTip="Save File As...", 
                                triggered=self.saveFileAs
                            )
        self.fileMenu.addAction(self.saveAsAction)
        
        self.quitAction = QtGui.QAction(
                            QtGui.QIcon(':/images/save.png'), 
                            "&Quit RST Previewer", 
                            self,
                            shortcut="Ctrl+Q",
                            statusTip="Quit RST Previewer",
                            triggered=self.close
                        )        
        self.fileMenu.addAction(self.quitAction)

    def openFile(self, path=None):
        """ 
            Ask the user to open a file via the Open File dialog.
            Then open it in the tree, editor, and HTML preview windows.
        """
        if not path:
            dialog = OpenDialog()
            dialog.set_folders_only(False)
            path = dialog.getOpenFileName(self, "Open File",
                    '', "ReStructuredText Files (*.rst *.txt)")
    
        if path:
            file_path = Path(path[0])
            filename = file_path.name
            tree_dir = file_path.parent.absolute()
            self.handleFileChanged(tree_dir, filename)

    def saveFile(self):
        if self.file_path:
            text = self.editor.toPlainText()
            try:
                f = open(self.file_path.absolute(), "wb")
                f.write(text)
            except IOError:
                QMessageBox.information(self, "Unable to open file: %s" % self.file_path.absolute())
                
    def saveFileAs(self):
        filename, _ = QtGui.QFileDialog.getSaveFileName(self, 'Save File As',
                                '', "ReStructuredText Files (*.rst *.txt)")
        if filename:
            text = self.editor.toPlainText()
            try:
                f = open(filename, "wb")
                f.write(text)
            except IOError:
                QMessageBox.information(self, "Unable to open file: %s" % filename)
    
    def openFolder(self, path=None):
        """ 
            Ask the user to open a folder (directory) via 
            the Open Folder dialog. Then open it in the tree, 
            editor, and HTML preview windows.
        """
        if not path:
            dialog = OpenDialog()
            dialog.set_folders_only(True)
            path = dialog.getExistingDirectory(self, "Open Folder", '')
        
        if path:                
            self.handleFileChanged(path)

    def handleFileChanged(self, dir, filename=None):
        """
            This is called whenever the active file is changed.
            It sets the tree, editor, and preview panes to the new file.
        """
        if not filename:
            # TODO: find first rst file if index.rst doesn't exist.
            filename = "index.rst"
            
        self.file_path = Path(dir, filename)
        
        # Load the file into the editor
        self.editor.open_file(self.file_path)
        
        # Load the directory containing the file into the tree.
        self.tree.load_from_dir(dir)
        
        # Load corresponding HTML file from pre-built Sphinx docs
        file_stem = str(self.file_path.stem)
        html_str = "_build/html/{0}.html".format(file_stem)
        output_html_path = Path(dir, html_str).absolute()
        self.preview.load_html(output_html_path)