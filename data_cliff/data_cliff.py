from difflib import unified_diff
from hashlib import md5
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

from data_cliff.getter import get_data


def compare(before_rev: str, after_rev: Optional[str], data_path: str) -> int:
    with TemporaryDirectory() as tmp_path:
        before_path = tmp_path + "a"
        after_path = tmp_path + "b"
        success = get_data(before_rev, data_path, local_path=before_path)
        success |= get_data(after_rev, data_path, local_path=after_path)

        if not success:
            return _error_retrieving_data(data_path)
        _diff_files(before_path, after_path, data_path=data_path)
        return 0


def _diff_files(before_path: str, after_path: str, data_path: str) -> None:
    if Path(before_path).is_file() or Path(after_path).is_file():
        return _diff_file(
            before_file_path=before_path,
            after_file_path=after_path,
            file_name=data_path,
        )
    files = set(
        file.relative_to(x_path)
        for x_path in [before_path, after_path]
        for file in Path(x_path).iterdir()
    )
    for file in files:
        _diff_files(
            before_path=f"{before_path}/{file}",
            after_path=f"{after_path}/{file}",
            data_path=f"{data_path}/{file}",
        )


def _diff_file(before_file_path: str, after_file_path: str, file_name: str) -> None:
    _assert_files_exist(before_file_path, after_file_path)
    try:
        _diff_text_file(before_file_path, after_file_path, file_name)
    except UnicodeDecodeError:
        _diff_binary_file(before_file_path, after_file_path, file_name)


def _assert_files_exist(before_file_path: str, after_file_path: str) -> None:
    _touch_if_does_not_exist(Path(before_file_path))
    _touch_if_does_not_exist(Path(after_file_path))


def _diff_text_file(
    before_file_path: str, after_file_path: str, file_name: str
) -> None:
    with open(before_file_path) as a, open(after_file_path) as b:
        diff_list = [
            _format_line(line)
            for line in unified_diff(
                a.read().splitlines(),
                b.read().splitlines(),
                fromfile=f"a/{file_name}",
                tofile=f"b/{file_name}",
            )
        ]

        header = _get_header(before_file_path, after_file_path, file_name)
        _display(diff_list, header)


def _diff_binary_file(
    before_file_path: str, after_file_path: str, file_name: str
) -> None:
    before_hash = _hash_file(before_file_path)
    after_hash = _hash_file(after_file_path)
    if before_hash != after_hash:
        header = _get_header(before_file_path, after_file_path, file_name)
        _display([f"Binary files a/{file_name} and b/{file_name} differ"], header)


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


def _get_header(before_path: str, after_path: str, file_name: str) -> str:
    return (
        f"cliff a/{file_name} b/{file_name}\n"
        f"index {_hash_file(before_path)}..{_hash_file(after_path)} "
        f"{_get_mode(file_name)}"
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
