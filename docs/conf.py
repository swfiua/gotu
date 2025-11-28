# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'gotu'
copyright = '2024, Johnny Gill'
author = 'Johnny Gill'

# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
    #'sphinxcontrib.collections',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static', '../html', '_collections']

# Collections extension.
# I am (mis)using this to expand a template a bunch of times so
# I can generate a bunch of static html pages that use pyodide
# to make all this come alive in the browser.
collections = {
    'magic': {
        'driver': 'jinja',
        'source': '_templates/magic.html',
        'target': '{{module|lower}}_{{class|lower}}.html',
        'multiple_files': True,
        'final_clean': False,
        'data': [
            {
               'module': 'wits',
               'class': 'SolarSystem',
            },
            {
               'module': 'spiral',
               'class': 'Spiral',
            },
            {
               'module': 'spiral',
               'class': 'SkyMap',
            },
        ],
    },
}


intersphinx_mapping = {
    'Pillow': ('https://pillow.readthedocs.io/en/stable/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'cycler': ('https://matplotlib.org/cycler/', None),
    'dateutil': ('https://dateutil.readthedocs.io/en/stable/', None),
    'ipykernel': ('https://ipykernel.readthedocs.io/en/latest/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'pytest': ('https://pytest.org/en/stable/', None),
    'python': ('https://docs.python.org/3/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
    'tornado': ('https://www.tornadoweb.org/en/stable/', None),
    'xarray': ('https://docs.xarray.dev/en/stable/', None),
    'meson-python': ('https://meson-python.readthedocs.io/en/stable/', None),
    'blume': ('https://blume.readthedocs.io/en/latest/', None),
    'astropy': ('https://astropy.readthedocs.io/en/stable/', None),
    'healpy': ('https://healpy.readthedocs.io/en/stable/', None),
    'pip': ('https://pip.pypa.io/en/stable/', None),
}
