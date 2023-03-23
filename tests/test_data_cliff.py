import json
from pathlib import Path


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
    _add_line_to_path(file)

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

    # When
    compare("HEAD", None, str(file))
    stdout, _ = capsys.readouterr()

    # Then
    assert stdout == expected_output

    # Finally
    DVCFileSystem(rev="HEAD").get(str(file), str(file))


def test_compare_staged_change_on_folder(dvc_path, capsys) -> None:
    # Given
    from dvc.api import DVCFileSystem

    from data_cliff.data_cliff import compare

    folder = dvc_path / "dir"
    _add_line_to_path(folder / "file.json")

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

    # When
    compare("HEAD", None, str(folder))
    stdout, _ = capsys.readouterr()

    # Then
    assert stdout == expected_output

    # Finally
    DVCFileSystem(rev="HEAD").get(str(folder), str(folder), recursive=True)


def _add_line_to_path(file: Path) -> None:
    with open(file) as fid:
        parsed_json = json.load(fid)

    parsed_json["new_key"] = "new_value"

    with open(file, "w") as outid:
        json.dump(parsed_json, outid, indent=4)
