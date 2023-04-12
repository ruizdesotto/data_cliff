import sys
import warnings

from data_cliff.arg_parse import parse_args
from data_cliff.data_cliff import compare


def main() -> int:
    """Console script for data_cliff."""
    args = parse_args(sys.argv[1:])

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return compare(
            before_rev=args.before_rev,
            after_rev=args.after_rev,
            data_path=args.data_path,
        )


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
