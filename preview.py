from PySide import QtGui, QtCore, QtWebKit
from unipath import Path


class Preview(QtWebKit.QWebView):
	def __init__(self, parent=None):
		super(Preview, self).__init__(parent)
		
		# TODO: Load HTML from real Sphinx output file
		output_html_path = Path("testfiles/contributing.html").absolute()
		self.load(QtCore.QUrl.fromLocalFile(output_html_path))