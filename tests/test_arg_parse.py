from contextlib import nullcontext
from typing import ContextManager

import pytest

from data_cliff.arg_parse import CLIException


@pytest.mark.parametrize(
    "args, a_rev, b_rev, data_path",
    [
        ([], "HEAD", None, ""),
        (["HEAD~"], "HEAD~", None, ""),
        (["path/to/file"], "HEAD", None, "path/to/file"),
        (["HEAD~", "path/to/file"], "HEAD~", None, "path/to/file"),
        (["HEAD~", "HEAD", "path/to/file"], "HEAD~", "HEAD", "path/to/file"),
    ],
)
def test_parse_args(args: list[str], a_rev: str, b_rev: str, data_path: str) -> None:
    # Given
    from data_cliff.arg_parse import _Args, parse_args

    # When
    parsed_args = parse_args(args)

    # Then
    assert isinstance(parsed_args, _Args)
    assert parsed_args.a_rev == a_rev
    assert parsed_args.b_rev == b_rev
    assert parsed_args.data_path == data_path


@pytest.mark.parametrize(
    "args, expectation",
    [
        ([], nullcontext()),
        (["HEAD~", "HEAD"], nullcontext()),
        (["HEAD~", "HEAD", "path/to/file"], nullcontext()),
        (
            ["HEAD~", "HEAD", "path/to/file", "unrecognized"],
            pytest.raises(CLIException),
        ),
    ],
)
def test_parse_command_line_raw_args(args: list[str], expectation: ContextManager):
    # Given
    from data_cliff.arg_parse import parse_command_line_raw_args

    # When / Then
    with expectation:
        parse_command_line_raw_args(args)
