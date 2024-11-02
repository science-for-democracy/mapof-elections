# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
# sys.path.insert(0, os.path.abspath(os.path.join("..","..","src","mapof")))
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "src")))

project = 'mapof-elections'
copyright = '2024, Stanisław Szufa and Andrzej Kaczmarczyk'
author = 'Stanisław Szufa and Andrzej Kaczmarczyk'
release = '2024'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.imgmath",
    'sphinx.ext.intersphinx'
]


add_module_names = False
autodoc_member_order = "groupwise"
autodoc_typehints_format = "short"
python_use_unqualified_type_names = True

napoleon_google_docstring = False
napoleon_custom_sections = ["Validation"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]



source_suffix = ".rst"
master_doc = "index"

# version = prefsampling.__version__
# release = prefsampling.__version__
language = "en"

pygments_style = "sphinx"

doctest_path = [".."]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
# html_static_path = ['_static']
# html_css_files = [
#     'custom.css',
# ]

html_title = "Map of Elections"
html_theme_options = {
    "repository_url": "https://github.com/science-for-democracy/mapof-elections",
    "use_repository_button": True,
    "navigation_with_keys": True,
}


intersphinx_mapping = {
    'prefsampling': ('https://comsoc-community.github.io/prefsampling/', None),
}
