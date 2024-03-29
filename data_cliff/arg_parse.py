import argparse
from dataclasses import dataclass
from typing import Optional

from pygit2 import Repository, RevSpec


class CLIException(Exception):
    pass


@dataclass(frozen=True)
class _Args:
    before_rev: str
    after_rev: Optional[str]
    data_path: str


def parse_args(args: list[str]) -> _Args:
    raw_args = parse_command_line_raw_args(args)
    before_rev = raw_args.pos_1 if _is_git_rev(raw_args.pos_1) else "HEAD"
    after_rev = raw_args.pos_2 if _is_git_rev(raw_args.pos_2) else None
    data_path = _get_data_path(raw_args)
    return _Args(before_rev=before_rev, after_rev=after_rev, data_path=data_path)


def parse_command_line_raw_args(args: list[str]) -> argparse.Namespace:
    raw_parser = _cli_parse_factory()
    try:
        return raw_parser.parse_args(args)
    except SystemExit:
        raise CLIException(raw_parser.usage)


def _is_git_rev(rev: Optional[str]) -> bool:
    if rev is None:
        return False
    try:
        return isinstance(Repository(".").revparse(rev.rstrip("/")), RevSpec)
    except KeyError:
        return False


def _get_data_path(raw_args: argparse.Namespace):
    for arg in [raw_args.pos_1, raw_args.pos_2, raw_args.pos_3]:
        if arg is not None and not _is_git_rev(arg):
            return arg
    return ""


def _cli_parse_factory() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("pos_1", nargs="?", default=None)
    parser.add_argument("pos_2", nargs="?", default=None)
    parser.add_argument("pos_3", nargs="?", default=None)
    return parser
