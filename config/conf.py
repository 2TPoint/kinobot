# -*- coding: utf-8 -*-
#
# kinobot documentation build configuration file, created by
# sphinx-quickstart on Sat Mar 27 15:14:35 2023.
#

# -- Project information -----------------------------------------------------

project = 'kinobot'
author = 'Fedor Shmakov, Nikolay Khorov, Ivan Demin'
release = '0.0.1'

# -- General configuration ---------------------------------------------------

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'alabaster'

# -- Options for HTML output -------------------------------------------------

html_static_path = ['_static']