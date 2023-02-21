#!/usr/bin/env python

"""Tests for `data_cliff` package."""

import pytest


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_bare_example():
    # Given
    from dvc.api import DVCFileSystem

    # from data_cliff.data_cliff import compare
    # a_rev = "b0660085fd6990399379d81d41ce2be7fcae643e"
    # b_rev = "873afcd844f6a3c77c9661135138e619ba11b11f"
    file = "tests/dvc_test_data/dir1/file.test"
    a_fs = DVCFileSystem(rev="HEAD")
    a_fs.get(file, "zzzzzzzzzzzzzz")

    # When
    # compare(a_rev, b_rev, file)

    # Assert
    pass
