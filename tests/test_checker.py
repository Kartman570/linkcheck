import tempfile
import unittest
from pathlib import Path
from linkcheck.checker import check_tree


class CheckerTests(unittest.TestCase):
    def test_paths_and_anchors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.md").write_text(
                "[ok](other.md#part) [bad](other.md#absent) [lost](missing.md)")
            (root / "other.md").write_text("# Part\n")
            failures = check_tree(root)
            self.assertEqual(len(failures), 2)
            self.assertEqual({x['reason'] for x in failures},
                             {"anchor does not exist", "file does not exist"})

    def test_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("[bad](../secret.md)")
            self.assertEqual(check_tree(root)[0]['reason'], "outside documentation root")

    def test_encoded_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("[ok](two%20words.md)")
            (root / "two words.md").write_text("# Text")
            self.assertEqual(check_tree(root), [])
