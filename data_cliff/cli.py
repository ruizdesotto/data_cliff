import warnings

from data_cliff.arg_parse import parse_args
from data_cliff.data_cliff import compare


def _main(raw_args: list[str]) -> int:
    """Console script for data_cliff."""
    args = parse_args(raw_args)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        compare(a_rev=args.a_rev, b_rev=args.b_rev, data_path=args.data_path)
    return 0


if __name__ == "__main__":  # pragma: no cover
    import sys

    sys.exit(_main(sys.argv[1:]))
