import io
import json
from pathlib import Path
from unittest.mock import patch


def test_main(dvc_path, captured_print: io.StringIO) -> None:
    # Given
    import sys

    from dvc.api import DVCFileSystem

    from data_cliff.cli import main

    file = dvc_path / "dir" / "file.json"
    test_args = ["cliff", str(file)]
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
    with patch.object(sys, "argv", test_args):
        main()

    # Then
    assert captured_print.getvalue() == expected_output

    # Finally
    DVCFileSystem(rev="HEAD").get(str(file), str(file))


def _add_line_to_path(file: Path) -> None:
    with open(file) as fid:
        parsed_json = json.load(fid)

    parsed_json["new_key"] = "new_value"

    with open(file, "w") as outid:
        json.dump(parsed_json, outid, indent=4)
