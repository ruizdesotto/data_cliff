#!/usr/bin/env python

"""Tests for `data_cliff` package."""

import shutil
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def setup_local_remote() -> None:
    tmp_remote = Path("/tmp/data_cliff_remote_data")
    shutil.rmtree(tmp_remote, ignore_errors=True)
    shutil.copytree("tests/test_dvc_data/remote_data", tmp_remote)


@pytest.fixture(scope="session")
def dvc_path() -> Path:
    return Path("tests") / "test_dvc_data" / "local_data"


def test_retrieves_file(dvc_path: Path, tmp_path: Path):
    # Given
    from dvc.api import DVCFileSystem

    a_fs = DVCFileSystem(rev="HEAD")
    file = dvc_path / "dir" / "file.json"
    out_file = tmp_path / "file.json"

    # When
    a_fs.get(str(file), str(out_file))

    # Then
    assert out_file.is_file()
