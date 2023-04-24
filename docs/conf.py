# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
# html_sidebars = {
#     '**': [
#         'about.html',
#         'navigation.html',
#         'relations.html',  # needs 'show_related': True theme option to display
#         'searchbox.html',
#         'donate.html',
#     ]
# }
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'sphinx.ext.githubpages']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'kinobot'
copyright = '2023'
author = 'Fedor Shmakov, Nikolay Khorov, Ivan Demin'
version = '1.0.0'
release = '1.0.0'
html_static_path = ['_static']
html_search_enabled=True
