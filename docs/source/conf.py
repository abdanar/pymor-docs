# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------
project = 'pyMOR Documentation Fork'
copyright = '2026, Anar Abdullayev'
author = 'Anar Abdullayev'
version = '0.1'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "numpydoc",
]

autosummary_generate = True
autosummary_imported_members = True
autosummary_use_toctree = True
add_module_names = False

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "imported-members": True,
}

numpydoc_show_class_members = False
numpydoc_show_inherited_class_members = False

templates_path = []
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_show_sourcelink = False

html_theme_options = {
    "logo": {
        "image_light": "_static/logo.svg",
        "image_dark": "_static/logo_dark.svg",
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