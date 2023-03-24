from dvc.api import DVCFileSystem


def get_data(rev: str | None, data_path: str, local_path: str) -> bool:
    try:
        fs = DVCFileSystem(rev=rev)
        fs.get(data_path, local_path, recursive=_is_directory(fs, data_path))
        return True
    except FileNotFoundError:
        return False


def _is_directory(fs: DVCFileSystem, data_path: str) -> bool:
    is_directory: bool = fs.info(str(data_path))["type"] == "directory"
    return is_directory
