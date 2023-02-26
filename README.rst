==========
Data Cliff
==========


.. image:: https://img.shields.io/pypi/v/data_cliff.svg
    :target: https://pypi.python.org/pypi/data_cliff

.. image:: https://img.shields.io/pypi/pyversions/data_cliff
    :target: https://pypi.python.org/pypi/data_cliff
    :alt: Python Version

.. image:: https://img.shields.io/pypi/dm/data_cliff.svg
    :target: https://pypi.python.org/pypi/data_cliff/
    :alt: PyPI download month

.. image:: https://img.shields.io/pypi/l/data_cliff.svg
    :target: https://pypi.python.org/pypi/data_cliff/
    :alt: Licence

.. image:: https://readthedocs.org/projects/data-cliff/badge/?version=latest
    :target: https://data-cliff.readthedocs.io/en/latest/?version=latest
    :alt: Documentation Status

.. .. image:: https://pyup.io/repos/github/ruizdesotto/data_cliff/shield.svg
..     :target: https://pyup.io/repos/github/ruizdesotto/data_cliff/
..     :alt: Updates

.. image:: https://github.com/ruizdesotto/data_cliff/actions/workflows/pypi_release.yml/badge.svg
    :target: https://github.com/ruizdesotto/data_cliff/actions?query=branch%3Amain
    :alt: Build Status

.. image:: https://github.com/ruizdesotto/data_cliff/actions/workflows/github-actions-pr.yml/badge.svg
    :target: https://github.com/ruizdesotto/data_cliff/actions?query=branch%3Amain
    :alt: CI Status

.. image:: https://codecov.io/gh/ruizdesotto/data_cliff/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/ruizdesotto/data_cliff
    :alt: Coverage

.. image:: http://www.mypy-lang.org/static/mypy_badge.svg
    :target: http://mypy-lang.org/
    :alt: mypy

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: black


CLI tool to show differences on text data tracked by dvc.


* Free software: Apache Software License 2.0
* Documentation: https://data-cliff.readthedocs.io.


Installation
------------

You can install the tool directly from ``pip``::

    pip install data_cliff


Quick start-guide
-----------------

``data_cliff`` is a tool that helps you visualize differences on text file you're
tracking on a ``dvc`` repo. Its CLI ``cliff`` aims to be as closed to ``git diff``
as possible::

    cliff [a_rev] [b_rev] [path/to/file]


``WARNING`` You must be in a `dvc` repository.



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
