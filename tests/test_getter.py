from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "file_name, expected",
    [
        ("file.json", True),
        ("fake_file.json", False),
    ],
)
def test_retrieves_file(
    file_name: str, expected: bool, dvc_path: Path, tmp_path: Path
) -> None:
    # Given
    from data_cliff.getter import get_data

    file = dvc_path / "dir" / file_name
    out_file = tmp_path / file_name

    # When / Then
    success = get_data(rev="HEAD", data_path=str(file), local_path=str(out_file))
    assert success == expected
    assert out_file.is_file() if success else True
