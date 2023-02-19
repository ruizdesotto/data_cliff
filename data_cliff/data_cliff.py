from difflib import unified_diff
from pathlib import Path
from tempfile import TemporaryDirectory

from dvc.api import DVCFileSystem


def compare(file_path: Path) -> None:
    a_rev = "HEAD"
    b_rev = None
    a_fs = DVCFileSystem(rev=a_rev)
    b_fs = DVCFileSystem(rev=b_rev)
    with TemporaryDirectory() as tmp_path:
        a_path = tmp_path + "a"
        b_path = tmp_path + "b"
        a_fs.get(file_path, a_path)
        b_fs.get(file_path, b_path)

        with open(a_path) as a, open(b_path) as b:
            for line in unified_diff(a.read().splitlines(), b.read().splitlines()):
                print(line)
