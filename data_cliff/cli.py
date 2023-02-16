"""Console script for data_cliff."""
import argparse
import sys
import warnings

from data_cliff.data_cliff import compare


def main():
    """Console script for data_cliff."""
    parser = argparse.ArgumentParser()
    parser.add_argument("_", nargs="*")
    args = parser.parse_args()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        compare(args._[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
