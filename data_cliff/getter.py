import shutil
from pathlib import Path
from typing import Optional

from dvc.api import DVCFileSystem


def get_data(rev: Optional[str], data_path: str, local_path: str) -> bool:
    if rev is None:
        return get_from_workdir(data_path, local_path)
    try:
        fs = DVCFileSystem(rev=rev)
        fs.get(data_path, local_path, recursive=_is_directory(fs, data_path))
        return True
    except FileNotFoundError:
        return False


def get_from_workdir(data_path: str, local_path: str) -> bool:
    if Path(data_path).is_file():
        shutil.copy(data_path, local_path)
        return True
    elif Path(data_path).is_dir():
        shutil.copytree(data_path, local_path)
        return True
    return False


def _is_directory(fs: DVCFileSystem, data_path: str) -> bool:
    is_directory: bool = fs.info(str(data_path))["type"] == "directory"
    return is_directory
