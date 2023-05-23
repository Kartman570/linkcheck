import argparse
import json
import sys
from pathlib import Path
from .checker import check_tree


def main():
    parser = argparse.ArgumentParser(description="Check Markdown links")
    parser.add_argument("root", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error("root must be a directory")
    try:
        failures = check_tree(args.root)
    except (OSError, UnicodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(failures, indent=2))
    else:
        for failure in failures:
            print("{file}: {target}: {reason}".format(**failure))
        print("%d broken links" % len(failures))
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
