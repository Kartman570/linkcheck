from pathlib import Path
from urllib.parse import unquote, urlsplit
from .markdown import anchors, links, reference_links


def check_file(path, root):
    path, root = Path(path).resolve(), Path(root).resolve()
    text = path.read_text(encoding="utf-8")
    failures = []
    for _, target in links(text) + reference_links(text):
        parsed = urlsplit(target)
        if parsed.scheme == "missing-reference":
            failures.append({"file": str(path.relative_to(root)), "target": target,
                             "reason": "undefined reference"})
            continue
        if parsed.scheme or parsed.netloc:
            continue
        dest = (root / unquote(parsed.path).lstrip("/") if parsed.path.startswith("/")
                else path.parent / unquote(parsed.path)) if parsed.path else path
        dest = dest.resolve()
        reason = None
        if root != dest and root not in dest.parents:
            reason = "outside documentation root"
        elif not dest.exists():
            reason = "file does not exist"
        elif parsed.fragment and dest.suffix.lower() in (".md", ".markdown"):
            if unquote(parsed.fragment) not in anchors(dest.read_text(encoding="utf-8")):
                reason = "anchor does not exist"
        if reason:
            failures.append({"file": str(path.relative_to(root)), "target": target,
                             "reason": reason})
    return failures


def check_tree(root):
    root = Path(root).resolve()
    failures = []
    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        if path.is_symlink():
            continue
        failures.extend(check_file(path, root))
    return failures
