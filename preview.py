from PySide import QtGui, QtCore, QtWebKit


class Preview(QtWebKit.QWebView):
	def __init__(self, parent=None):
		super(Preview, self).__init__(parent)
		self.load(QtCore.QUrl.fromLocalFile("/Users/audreyr/code/pydream-repos/rstpreviewer/testfiles/contributing.html"))