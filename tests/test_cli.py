import json
from pathlib import Path


def test__main(dvc_path, capsys) -> None:
    # Given
    from data_cliff.cli import _main

    file = dvc_path / "dir" / "file.json"
    _add_line_to_path(file)

    expected_output = (
        '--- \n\n+++ \n\n@@ -1,3 +1,4 @@\n\n {\n-    "test": "file"'
        '\n+    "test": "file",\n+    "new_key": "new_value"\n }\n'
    )

    # When
    _main([str(file)])
    stdout, _ = capsys.readouterr()

    # Then
    assert stdout == expected_output


def _add_line_to_path(file: Path) -> None:
    with open(file) as fid:
        parsed_json = json.load(fid)

    parsed_json["new_key"] = "new_value"

    with open(file, "w") as outid:
        json.dump(parsed_json, outid, indent=4)
