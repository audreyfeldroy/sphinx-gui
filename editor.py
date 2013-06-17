from PySide import QtCore, QtGui


class Editor(QtGui.QTextEdit):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)

    def open_file(self, file_path):
        inFile = QtCore.QFile(file_path.absolute())
        if inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            text = inFile.readAll()
        
            try:
                # Python v3.
                text = str(text, encoding='ascii')
            except TypeError:
                # Python v2.
                text = str(text)
        
            self.setPlainText(text)
