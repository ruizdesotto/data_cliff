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

        _diff_files(a_path, b_path)


def _diff_files(a_path: str, b_path: str) -> None:
    with open(a_path) as a, open(b_path) as b:
        diff_list = [
            _format_line(line)
            for line in unified_diff(a.read().splitlines(), b.read().splitlines())
        ]

        _display(diff_list)


def _format_line(line: str) -> str:
    line = line.rstrip("\n")
    if line.startswith("+++") or line.startswith("---"):
        return line

    if line.startswith("+"):
        return _green_line(line)
    if line.startswith("-"):
        return _red_line(line)
    return line


def _red_line(line: str) -> str:
    return f"\033[91m{line}\033[00m"


def _green_line(line: str) -> str:
    return f"\033[92m{line}\033[00m"


def _display(diff: list[str]) -> None:
    print("\n".join(diff))
