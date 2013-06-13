from PySide import QtGui, QtCore

from editor import Editor


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        treeview =  QtGui.QTreeView()
        editor = Editor()
        self.setCentralWidget(splitter)

        splitter.addWidget(treeview)
        splitter.addWidget(editor)

        self.setWindowTitle("RST Previewer")
        self.showMaximized()
