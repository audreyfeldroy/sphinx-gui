from PySide import QtGui, QtCore


class OpenDialog(QtGui.QFileDialog):
	def __init__(self, parent=None):
		super(OpenDialog, self).__init__()

	def set_folders_only(self, is_folders_only):
		if is_folders_only:
			self.setFileMode(self.Directory)
			self.setOption(self.ShowDirsOnly, True)
		else:
			self.setFileMode(self.AnyFile)
			self.setOption(self.ShowDirsOnly, False)
			self.setNameFilter('All files (*)')
