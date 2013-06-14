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
		
	def load_from_path(self, path):
		""" Load directory containing file into the tree. """
		
		# Link the tree to a model
		model = QtGui.QFileSystemModel()
		model.setRootPath(path)
		self.setModel(model)
		
		# Set the tree's index to the root of the model
		indexRoot = model.index(model.rootPath())
		self.setRootIndex(indexRoot)

		# Display tree cleanly
		self.hide_unwanted_info()

	def hide_unwanted_info(self):
		""" Hides unneeded columns and header. """		
		
		# Hide tree size and date columns
		self.hideColumn(1)
		self.hideColumn(2)
		self.hideColumn(3)
		
		# Hide tree header
		self.setHeaderHidden(True)
