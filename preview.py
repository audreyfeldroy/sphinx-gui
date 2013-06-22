from PySide import QtGui, QtCore, QtWebKit
from unipath import Path


class Preview(QtWebKit.QWebView):
	def __init__(self, parent=None):
		super(Preview, self).__init__(parent)
		
	def load_html(self, path):
		"""
			Load the specified HTML file into the preview pane.
		"""
		self.load(QtCore.QUrl.fromLocalFile(path))
		
		
		
class PDFPane(QtWebKit.QWebView):
	def __init__(self, parent=None):
		super(PDFPane, self).__init__(parent)
		self.path = None

	def load_pdf(self, path=None):
		"""
			Load the specified HTML file into the preview pane.
		"""
		if path:
			self.path = path
		self.load(QtCore.QUrl.fromLocalFile(self.path))
