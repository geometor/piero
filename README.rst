=====
piero
=====

Folio-verified Digital Scriptorium codex of Libellus de Quinque Corporibus Regularibus by Piero della Francesca

Edition Overview
----------------

- **Treatise**: *Libellus de Quinque Corporibus Regularibus*
- **Author**: Piero della Francesca
- **Primary Edition Track**: ``docsrc/quinque_corporibus/`` (``:layout: book``)
- **Apparatus**: ``resources/persons.json``, ``resources/citations.json``, ``resources/glossary.json``
Installation & Verification
---------------------------

Managed with ``uv`` on Python 3.13:

.. code-block:: bash

   uv run --no-sync pytest
   ruff check src tests demos
   publish build

Usage
-----

.. code-block:: bash

   piero --help

Links
-----

- **Documentation**: https://geometor.github.io/piero
- **Repository**: https://github.com/geometor/piero
- **Issues**: https://github.com/geometor/piero/issues

License
-------

Licensed under the MIT License. See ``LICENSE`` for details.
