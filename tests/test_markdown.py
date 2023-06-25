import unittest
from linkcheck.markdown import anchors, links, reference_links


class MarkdownTests(unittest.TestCase):
    def test_code_fence(self):
        self.assertEqual(links("```md\n[x](missing)\n```\n[x](ok)"), [(1, "ok")])

    def test_duplicate_headings(self):
        self.assertEqual(anchors("# Hello!\n# Hello!\n"), {"hello", "hello-1"})

    def test_reference(self):
        result = reference_links("[Read][guide]\n[guide]: doc.md")
        self.assertEqual(result[0][1], "doc.md")

    def test_missing_reference(self):
        self.assertEqual(reference_links("[Read][missing]")[0][1], "missing-reference:missing")
