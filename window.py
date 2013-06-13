from PySide import QtGui

from editor import Editor


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        editor = Editor()
        self.setCentralWidget(editor)
        self.setWindowTitle("RST Previewer")
        self.showMaximized()
