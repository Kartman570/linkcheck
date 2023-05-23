import argparse
import json
import sys
from pathlib import Path
from .checker import check_tree
from .markdown import links, reference_links
from .network import check_url


def main():
    parser = argparse.ArgumentParser(description="Check Markdown links")
    parser.add_argument("root", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--http", action="store_true", help="Also request HTTP links")
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error("root must be a directory")
    try:
        failures = check_tree(args.root)
        if args.http:
            cache = {}
            for path in sorted(args.root.rglob("*.md")):
                if path.is_symlink():
                    continue
                text = path.read_text(encoding="utf-8")
                for _, target in links(text) + reference_links(text):
                    if target.startswith(("http://", "https://")):
                        if target not in cache:
                            cache[target] = check_url(target)
                        if cache[target][1]:
                            failures.append({"file": str(path.relative_to(args.root)),
                                             "target": target, "reason": cache[target][1]})
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
