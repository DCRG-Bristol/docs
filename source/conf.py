import os
import sys
sys.path.insert(0, os.path.abspath('.'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'DCRG Docs'
copyright = '2025, Fintan Healy'
author = 'Fintan Healy'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.napoleon',          # For Google/NumPy style docstrings
    'sphinx.ext.autodoc',           # For automatic documentation
    'sphinxcontrib.matlab',         # MATLAB domain support
]

# Napoleon settings (tweaked for MATLAB-style documentation)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = False  # So that return type lines don’t get repeated
napoleon_custom_sections = [('Returns', 'params_style')]

autosummary_generate = True
html_theme_options = {'navigation_depth': 6}

# -- sphinxcontrib-matlabdomain settings ------------------------------------

# Path to your MATLAB source code (absolute or relative to conf.py)
matlab_src_dir = os.path.abspath('../tbxs')  # e.g., if source is in ../matlab
primary_domain = 'mat'
matlab_short_links = True
matlab_auto_link = "basic"
# The name of the root module/package (e.g. a folder containing +myPackage)
matlab_keep_package_prefix = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
# html_static_path = ['_static']