import argparse
from dataclasses import dataclass

from pygit2 import Repository, RevSpec


class CLIException(Exception):
    pass


@dataclass(frozen=True)
class _Args:
    a_rev: str
    b_rev: str | None
    data_path: str


def parse_args(args: list[str]) -> _Args:
    raw_args = parse_command_line_raw_args(args)
    a_rev = raw_args.pos_1 if _is_git_rev(raw_args.pos_1) else "HEAD"
    b_rev = raw_args.pos_2 if _is_git_rev(raw_args.pos_2) else None
    data_path = _get_data_path(raw_args)
    return _Args(a_rev=a_rev, b_rev=b_rev, data_path=data_path)


def parse_command_line_raw_args(args: list[str]) -> argparse.Namespace:
    raw_parser = _cli_parse_factory()
    try:
        return raw_parser.parse_args(args)
    except SystemExit:
        raise CLIException(raw_parser.usage)


def _is_git_rev(rev: str | None) -> bool:
    if rev is None:
        return False
    try:
        return isinstance(Repository(".").revparse(rev), RevSpec)
    except KeyError:
        return False


def _get_data_path(raw_args: argparse.Namespace):
    if not _is_git_rev(raw_args.pos_1) and raw_args.pos_1 is not None:
        return raw_args.pos_1
    elif not _is_git_rev(raw_args.pos_2) and raw_args.pos_2 is not None:
        return raw_args.pos_2
    elif not _is_git_rev(raw_args.pos_3) and raw_args.pos_3 is not None:
        return raw_args.pos_3
    else:
        return ""


def _cli_parse_factory() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("pos_1", nargs="?", default=None)
    parser.add_argument("pos_2", nargs="?", default=None)
    parser.add_argument("pos_3", nargs="?", default=None)
    return parser
