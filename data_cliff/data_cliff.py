from difflib import unified_diff
from hashlib import md5
from pathlib import Path
from tempfile import TemporaryDirectory

from data_cliff.getter import get_data


def compare(a_rev: str, b_rev: str | None, data_path: str) -> int:
    with TemporaryDirectory() as tmp_path:
        a_path = tmp_path + "a"
        b_path = tmp_path + "b"
        success = get_data(a_rev, data_path, local_path=a_path)
        success |= get_data(b_rev, data_path, local_path=b_path)

        if not success:
            return _error_retrieving_data(data_path)
        _diff_files(a_path, b_path, data_path=data_path)
        return 0


def _diff_files(a_path: str, b_path: str, data_path: str) -> None:
    if Path(a_path).is_file() or Path(b_path).is_file():
        return _diff_file(a_file_path=a_path, b_file_path=b_path, file_name=data_path)
    files = set(
        file.relative_to(x_path)
        for x_path in [a_path, b_path]
        for file in Path(x_path).iterdir()
    )
    for file in files:
        _diff_files(
            a_path=f"{a_path}/{file}",
            b_path=f"{b_path}/{file}",
            data_path=f"{data_path}/{file}",
        )


def _diff_file(a_file_path: str, b_file_path: str, file_name: str) -> None:
    _assert_files_exist(a_file_path, b_file_path)

    with open(a_file_path) as a, open(b_file_path) as b:
        diff_list = [
            _format_line(line)
            for line in unified_diff(
                a.read().splitlines(),
                b.read().splitlines(),
                fromfile=f"a/{file_name}",
                tofile=f"b/{file_name}",
            )
        ]

        header = _get_header(a_file_path, b_file_path, file_name)
        _display(diff_list, header)


def _assert_files_exist(a_file_path: str, b_file_path: str) -> None:
    _touch_if_does_not_exist(Path(a_file_path))
    _touch_if_does_not_exist(Path(b_file_path))


def _touch_if_does_not_exist(file_path: Path) -> None:
    if not file_path.exists():
        file_path.touch()


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


def _error_retrieving_data(data_path: str) -> int:
    print(f'Error: Path "{data_path}" not found.')
    return 1
