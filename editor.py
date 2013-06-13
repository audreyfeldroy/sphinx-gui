from PySide import QtGui


class Editor(QtGui.QTextEdit):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)

