# pyMOR Documentation Improvement Fork

This repository is a documentation-focused fork of the pyMOR project (see original project: https://github.com/pymor/pymor). The primary goal of this fork is to enhance the quality, structure, and usability of the pyMOR documentation without modifying the core scientific codebase. 


## Objectives

- improve Sphinx configuration and build reliability
- standardize docstring formatting using numpydoc conventions
- reduce documentation inconsistencies across modules
- improve API documentation structure and readability
- enhance navigation and cross-referencing
- experiment with cleaner and more modern documentation workflows

No changes are made to the core numerical algorithms or scientific implementation of pyMOR.

## Roadmap

- [ ] **Initial cleanup and standardization**
  - Refactor existing documentation for consistency
  - Improve Sphinx configuration and structure
  - Standardize docstring style

- [ ] **Enhanced API documentation**
  - Improve documentation of public modules, classes, and functions
  - Add clear examples where needed

- [ ] **Navigation and structure improvements**
  - Improve sidebar and table of contents structure
  - Strengthen cross-referencing between modules

- [ ] **Workflow improvements**
  - Explore CI-based documentation builds
  - Investigate automated documentation generation improvements
  
## Local Documentation Build

To build the documentation locally:

```bash
cd docs
make html
```

Then open the generated file in your browser:

```bash
docs/build/html/index.html
```

Open this file in any web browser to view the documentation.

## Development Notes

This repository is primarily maintained for personal and experimental documentation improvements. However, ideas and improvements that enhance clarity or usability may be considered for upstream contribution to the original pyMOR project.

## License

This repository follows the same license as the original pyMOR project unless otherwise stated.