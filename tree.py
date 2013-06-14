from PySide import QtGui, QtCore


class Tree(QtGui.QTreeView):
	def __init__(self, parent=None):
		super(Tree, self).__init__(parent)
		self.setMaximumWidth(250)
		
		# Get something to show up in tree
		# self.pathRoot = QtCore.QDir.rootPath()		
		# self.model = QtGui.QFileSystemModel(self)
		# self.model.setRootPath(self.pathRoot)
		# self.setModel(self.model)
		# self.indexRoot = self.model.index(self.model.rootPath())
		# self.setRootIndex(self.indexRoot)
		