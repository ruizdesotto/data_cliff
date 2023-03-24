import json
from pathlib import Path

import pytest


def test_retrieves_file(dvc_path: Path, tmp_path: Path) -> None:
    # Given
    from dvc.api import DVCFileSystem

    a_fs = DVCFileSystem(rev="HEAD")
    file = dvc_path / "dir" / "file.json"
    out_file = tmp_path / "file.json"

    # When
    a_fs.get(str(file), str(out_file))

    # Then
    assert out_file.is_file()


def test_compare_staged_change_on_single_file(dvc_path, capsys) -> None:
    # Given
    from dvc.api import DVCFileSystem

    from data_cliff.data_cliff import compare

    file = dvc_path / "dir" / "file.json"
    _add_key_to_json(file)

    expected_output = (
        "cliff a/tests/test_dvc_data/local_data/dir/file.json"
        " b/tests/test_dvc_data/local_data/dir/file.json\n"
        "index 612420a..db800ff 100644\n"
        "--- a/tests/test_dvc_data/local_data/dir/file.json\n"
        "+++ b/tests/test_dvc_data/local_data/dir/file.json\n"
        "@@ -1,3 +1,4 @@\n"
        " {\n"
        '\x1b[91m-    "test": "file"\x1b[00m\n'
        '\x1b[92m+    "test": "file",\x1b[00m\n'
        '\x1b[92m+    "new_key": "new_value"\x1b[00m\n'
        " }\n"
    )

    try:
        # When
        compare("HEAD", None, str(file))
        stdout, _ = capsys.readouterr()

        # Then
        assert stdout == expected_output
    finally:
        DVCFileSystem(rev="HEAD").get(str(file), str(file))


def test_compare_staged_change_on_folder(
    dvc_path: Path, capsys: pytest.CaptureFixture
) -> None:
    # Given
    from dvc.api import DVCFileSystem

    from data_cliff.data_cliff import compare

    folder = dvc_path / "dir"
    _add_key_to_json(folder / "file.json")

    expected_output = (
        "cliff a/tests/test_dvc_data/local_data/dir/file.json"
        " b/tests/test_dvc_data/local_data/dir/file.json\n"
        "index 612420a..db800ff 100644\n"
        "--- a/tests/test_dvc_data/local_data/dir/file.json\n"
        "+++ b/tests/test_dvc_data/local_data/dir/file.json\n"
        "@@ -1,3 +1,4 @@\n"
        " {\n"
        '\x1b[91m-    "test": "file"\x1b[00m\n'
        '\x1b[92m+    "test": "file",\x1b[00m\n'
        '\x1b[92m+    "new_key": "new_value"\x1b[00m\n'
        " }\n"
    )
    try:
        # When
        compare("HEAD", None, str(folder))
        stdout, _ = capsys.readouterr()

        # Then
        assert stdout == expected_output
    finally:
        DVCFileSystem(rev="HEAD").get(str(folder), str(folder), recursive=True)


def test_compare_staged_change_on_new_file(
    dvc_path: Path, capsys: pytest.CaptureFixture
) -> None:
    # Given

    from data_cliff.data_cliff import compare

    new_file = dvc_path / "dir" / "new_file.txt"
    new_file.touch()
    _add_line_to_file(new_file)

    expected_output = (
        "cliff a/tests/test_dvc_data/local_data/dir/new_file.txt"
        " b/tests/test_dvc_data/local_data/dir/new_file.txt\n"
        "index d41d8cd..426d316 100644\n"
        "--- a/tests/test_dvc_data/local_data/dir/new_file.txt\n"
        "+++ b/tests/test_dvc_data/local_data/dir/new_file.txt\n"
        "@@ -0,0 +1 @@\n"
        "\x1b[92m+new line\x1b[00m\n"
    )

    try:
        # When
        compare("HEAD", None, str(new_file))
        stdout, _ = capsys.readouterr()

        # Then
        assert stdout == expected_output
    finally:
        new_file.unlink()


def test_compare_on_non_existing_file(
    dvc_path: Path, capsys: pytest.CaptureFixture
) -> None:
    # Given

    from data_cliff.data_cliff import compare

    new_file = dvc_path / "dir" / "new_file.txt"

    expected_output = (
        'Error: Path "tests/test_dvc_data/local_data/dir/new_file.txt" not found.\n'
    )

    # When
    error_code = compare("HEAD", None, str(new_file))
    stdout, _ = capsys.readouterr()

    # Then
    assert error_code == 1
    assert stdout == expected_output


def _add_line_to_file(file: Path) -> None:
    with open(file) as fid:
        data = fid.readlines()

    data.append("new line\n")

    with open(file, "w") as outid:
        outid.write("".join(data))


def _add_key_to_json(file: Path) -> None:
    with open(file) as fid:
        parsed_json = json.load(fid)

    parsed_json["new_key"] = "new_value"

    with open(file, "w") as outid:
        json.dump(parsed_json, outid, indent=4)
