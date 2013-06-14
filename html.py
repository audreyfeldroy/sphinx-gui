from sphinx.application import Sphinx


def build_file():
	"""
		Builds the Sphinx docs for a hardcoded rst directory.
		TODO: get this working. 
	"""
	srcdir = "/Users/audreyr/code/pydream-repos/rstpreviewer/testfiles/rst/"
	confdir = "/Users/audreyr/code/pydream-repos/rstpreviewer/testfiles/"
	outdir = "/Users/audreyr/code/pydream-repos/rstpreviewer/testfiles/html/"
	doctreedir = "/Users/audreyr/code/pydream-repos/rstpreviewer/testfiles/"
	buildername = "html"
	
	sphinx_app = Sphinx(srcdir, confdir, outdir, doctreedir, buildername)
	sphinx_app.build()
	