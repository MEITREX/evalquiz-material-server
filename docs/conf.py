import os
import sys
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('../evalquiz_material_server'))

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_rtd_theme"]

html_theme = "sphinx_rtd_theme"
