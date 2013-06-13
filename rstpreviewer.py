#!/usr/bin/env python
import sys

from PySide import QtGui

from window import MainWindow

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
