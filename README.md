# linkcheck

Check local Markdown links and heading anchors before sharing a documentation folder.

## Usage

Requires Python 3.9 or newer, with no runtime dependencies.

```sh
python3 -m linkcheck examples/docs
python3 -m linkcheck examples/docs --json
python3 -m linkcheck examples/docs --http
```

Exit status is 0 for clean links, 1 for broken links and 2 for invalid input.
HTTP requests are opt-in. Local paths outside the supplied root are rejected.
Leading slashes are relative to the documentation root, not the filesystem.
Repeated heading anchors gain numeric suffixes. Query strings do not affect local
file lookup. Directory links are accepted; directory index pages are not inferred.

This intentionally supports a Markdown subset: ATX headings, inline links, full
and collapsed references, and HTML id/name attributes. It does not implement
CommonMark, shortcut references, nested link parentheses or setext headings.
Fenced blocks are skipped. Keep code examples inside fenced blocks.

## Development

```sh
python3 -m pip install -r requirements-dev.txt
make test
make lint
```

Network tests use a loopback server. The checker is for trusted documentation;
HTTP mode can reach any host accessible to your machine.
