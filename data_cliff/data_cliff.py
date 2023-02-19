from difflib import unified_diff
from pathlib import Path
from tempfile import TemporaryDirectory

from dvc.api import DVCFileSystem


def compare(a_rev: str, b_rev: str | None, data_path: str) -> None:
    a_fs = DVCFileSystem(rev=a_rev)
    b_fs = DVCFileSystem(rev=b_rev)
    if not Path(data_path).is_file():
        raise NotImplementedError("You're gonna have to wait for directories.")
    with TemporaryDirectory() as tmp_path:
        a_path = tmp_path + "a"
        b_path = tmp_path + "b"
        a_fs.get(data_path, a_path)
        b_fs.get(data_path, b_path)

        with open(a_path) as a, open(b_path) as b:
            for line in unified_diff(a.read().splitlines(), b.read().splitlines()):
                print(line)
