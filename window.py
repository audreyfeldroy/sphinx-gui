import os
import subprocess
import sys

from PySide import QtGui, QtCore
from unipath import Path

from dialogs import OpenDialog
from editor import Editor
from preview import Preview, PDFPane
from tree import Tree


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        # super(MainWindow, self).__init__(parent)
        if sys.platform == 'darwin':
            # Workaround for Qt issue on OS X that causes QMainWindow to
            # hide when adding QToolBar, see
            # https://bugreports.qt-project.org/browse/QTBUG-4300
            super(MainWindow, self).__init__(parent, QtCore.Qt.MacWindowToolBarButtonHint)
        else:
            super(MainWindow, self).__init__(parent)

    def setup_app(self):
        self.setupActions()
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.tree =  Tree()
        self.editor = Editor()

        self.tab_widget = QtGui.QTabWidget()
        self.preview = Preview()
        self.pdf_pane = PDFPane()
        self.tab_widget.addTab(self.preview, "HTML")
        self.tab_widget.addTab(self.pdf_pane, "PDF")

        self.file_path = None
        self.output_html_path = None

        self.setCentralWidget(splitter)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.editor)

        splitter.addWidget(self.tab_widget)
        # splitter.addWidget(self.preview)


        self.setWindowTitle("Sphinx Docs Editor")
        self.createMenus()
        self.createToolBars()
        self.showMaximized()

    def setupActions(self):
        """
            Set up the top menu actions and keyboard shortcuts.
        """

        # File Menu --------------------------------------------------
        self.openAction = QtGui.QAction(
                                # QtGui.QIcon(":/images/open.png"),
                                "&Open File",
                                self,
                                shortcut="Ctrl+O",
                                statusTip="Open File",
                                triggered=self.openFile
                            )



        self.openFolderAction = QtGui.QAction(
                                    # QtGui.QIcon(":/images/open.png"),
                                    "Open Folder",
                                    self,
                                    shortcut="Ctrl+Shift+O",
                                    statusTip="Open Folder",
                                    triggered=self.openFolder
                                )


        self.saveAction = QtGui.QAction(
                                # QtGui.QIcon(":/images/save.png"),
                                "&Save File",
                                self,
                                shortcut="Ctrl+S",
                                statusTip="Save File",
                                triggered=self.saveFile
                            )


        self.saveAsAction = QtGui.QAction(
                                # QtGui.QIcon(":/images/save.png"),
                                "Save As File",
                                self,
                                shortcut="Ctrl+Shift+S",
                                statusTip="Save File As...",
                                triggered=self.saveFileAs
                            )

        self.quitAction = QtGui.QAction(
                            # QtGui.QIcon(':/images/save.png'),
                            "&Quit",
                            self,
                            shortcut="Ctrl+Q",
                            statusTip="Quit",
                            triggered=self.close
                        )

        # Build Menu --------------------------------------------------

        self.buildHTMLAction = QtGui.QAction(
            "Build &HTML",
            self,
            shortcut="Ctrl+B",
            statusTip="Build HTML",
            triggered=self.buildHTML
        )

        self.buildPDFAction = QtGui.QAction(
            "Build &PDF",
            self,
            shortcut="Ctrl+Shift+B",
            statusTip="Build PDF",
            triggered=self.buildPDF
        )

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.openFolderAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)
        self.buildMenu = self.menuBar().addMenu("&Build")
        self.buildMenu.addAction(self.buildHTMLAction)
        self.buildMenu.addAction(self.buildPDFAction)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.openAction)
        self.fileToolBar.addAction(self.openFolderAction)
        self.fileToolBar.addAction(self.saveAction)
        # self.fileToolBar.addAction(self.saveAsAction)
        # self.fileToolBar.addAction(self.quitAction)
        self.buildToolBar = self.addToolBar("Build")
        self.buildToolBar.addAction(self.buildHTMLAction)
        self.buildToolBar.addAction(self.buildPDFAction)

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
                f.close()
                # self.rebuildHTML()
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
                f.close()
                # self.rebuildHTML()
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
        file_stem = str(self.file_path.stem)
        html_str = "_build/html/{0}.html".format(file_stem)
        self.output_html_path = Path(dir, html_str).absolute()

        # Load the file into the editor
        self.editor.open_file(self.file_path)

        # Load the directory containing the file into the tree.
        self.tree.load_from_dir(dir)

        # Load corresponding HTML file from pre-built Sphinx docs
        self.preview.load_html(self.output_html_path)

    def buildHTML(self):
        """
        Builds the .html version of the active file and reloads
        it in the preview pane.
        """

        # TODO: make this configurable via a dialog
        os.chdir(self.file_path.parent)
        proc = subprocess.Popen(["make", "clean"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in proc.stdout:
            print("stdout: " + line.rstrip())
        print('----------------')
        proc = subprocess.Popen(["make", "html"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc.wait()
        for line in proc.stdout:
            print("stdout: " + line.rstrip())

        # Load corresponding HTML file from newly-built Sphinx docs
        self.preview.load_html(self.output_html_path)

    def buildPDF(self):
        """
        Builds the .pdf version of the active file.
        """

        # TODO: get this working
        # TODO: make this configurable via a dialog
        os.chdir(self.file_path.parent)
        proc = subprocess.Popen(["make", "latexpdf"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc.wait()
        for line in proc.stdout:
            print("stdout: " + line.rstrip())
