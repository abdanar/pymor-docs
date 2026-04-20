# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pyMOR Documentation Fork'
copyright = '2026, Anar Abdullayev'
author = 'Anar Abdullayev'
version = '0.1'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "numpydoc",
]

autosummary_generate = True
numpydoc_show_class_members = False

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_show_sourcelink = False

html_theme_options = {
    "logo": {
        "image_light": "_static/logo.png",
        "image_dark": "_static/logo_dark.png",
    },

    "navigation_depth": 3,
    "show_toc_level": 2,

    "navbar_end": [
        "version-switcher",
        "theme-switcher",
        "navbar-icon-links",
    ],

    "switcher": {
        "json_url": "_static/versions.json",
        "version_match": release,
    },

    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/pymor/pymor",
            "icon": "fa-brands fa-github",
        },
    ],
}