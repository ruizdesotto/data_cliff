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
