from PySide import QtGui, QtCore


class Tree(QtGui.QTreeView):
	def __init__(self, parent=None):
		super(Tree, self).__init__(parent)
		self.dir_path = None

	def load_from_dir(self, dir_path):
		""" Load directory containing file into the tree. """
		
		# If it's the same dir as before, return to avoid redrawing
		if dir_path == self.dir_path:
			return
		
		# Store the path info
		self.dir_path = dir_path
		
		# Link the tree to a model
		model = QtGui.QFileSystemModel()
		model.setRootPath(dir_path)
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

	def selectionChanged(self, selected, deselected):
		""" 
			Event handler for selection changes.
			
			Triggers a fileChanged event in parent window.
		"""
		super(Tree, self).selectionChanged(selected, deselected)
		indexes = selected.indexes()
		if indexes:
			# Handle fileChanged event in main window
			new_filename = self.model().data(indexes[0])
			main_win = self.parent().parent()
			main_win.handleFileChanged(self.dir_path, new_filename)
			