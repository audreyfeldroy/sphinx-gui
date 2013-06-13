from PySide import QtGui


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("RST Previewer")
        self.showMaximized()
