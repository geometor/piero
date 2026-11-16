:navigation: header
:order: 10

=====
About
=====

``geometor.piero`` is developed and maintained by **phiarchitect** as part of the **GEOMETOR** organization.

Folio-verified Digital Scriptorium codex of Libellus de Quinque Corporibus Regularibus by Piero della Francesca

Repository Architecture
-----------------------

- **Python Package**: ``src/geometor/piero/`` (Python 3.13)
- **Codex Edition Track**: ``docsrc/quinque_corporibus/`` (``:layout: book``)
- **Scholarly Apparatus**: ``resources/persons.json``, ``resources/citations.json``, ``resources/glossary.json``
- **Automated Verification**: ``tests/`` (``pytest`` + ``ruff``) and ``docsrc/`` (``publish build``)
