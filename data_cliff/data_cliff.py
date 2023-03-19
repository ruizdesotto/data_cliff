from difflib import unified_diff
from hashlib import md5
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

        _diff_files(a_path, b_path, file_name=data_path)


def _diff_files(a_path: str, b_path: str, file_name: str) -> None:
    with open(a_path) as a, open(b_path) as b:
        diff_list = [
            _format_line(line)
            for line in unified_diff(
                a.read().splitlines(),
                b.read().splitlines(),
                fromfile=f"a/{file_name}",
                tofile=f"b/{file_name}",
            )
        ]

        header = _get_header(a_path, b_path, file_name)
        _display(diff_list, header)


def _format_line(line: str) -> str:
    line = line.rstrip("\n")
    if line.startswith("+++") or line.startswith("---"):
        return line

    if line.startswith("+"):
        return _green_line(line)
    if line.startswith("-"):
        return _red_line(line)
    return line


def _get_header(a_path: str, b_path: str, file_name: str) -> str:
    return (
        f"cliff a/{file_name} b/{file_name}\n"
        f"index {_hash_file(a_path)}..{_hash_file(b_path)} {_get_mode(file_name)}"
    )


def _hash_file(file_path: str) -> str:
    hash_md5 = md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()[:7]


def _get_mode(file_name: str) -> str:
    return oct(Path(file_name).stat().st_mode)[2:]


def _red_line(line: str) -> str:
    return f"\033[91m{line}\033[00m"


def _green_line(line: str) -> str:
    return f"\033[92m{line}\033[00m"


def _display(diff: list[str], header: str) -> None:
    if len(diff) == 0:
        return
    print(header)
    print("\n".join(diff))
