import io
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture(scope="session")
def setup_local_remote() -> None:
    tmp_remote = Path("/tmp/data_cliff_remote_data")
    shutil.rmtree(tmp_remote, ignore_errors=True)
    shutil.copytree("tests/test_dvc_data/remote_data", tmp_remote)


@pytest.fixture(scope="session")
def dvc_path() -> Path:
    return Path("tests") / "test_dvc_data" / "local_data"


@pytest.fixture
def captured_print():
    with io.StringIO() as output:
        with patch("builtins.print", new=lambda msg: output.write(f"{msg}\n")):
            yield output
