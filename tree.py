from PySide import QtGui


class Tree(QtGui.QTreeView):
	def __init__(self, parent=None):
		super(Tree, self).__init__(parent)
		self.setMaximumWidth(250)
