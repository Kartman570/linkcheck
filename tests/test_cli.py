import subprocess
import sys
import unittest


class CliTests(unittest.TestCase):
    def test_example_tree(self):
        result = subprocess.run([sys.executable, "-m", "linkcheck", "examples/docs", "--json"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[]")
