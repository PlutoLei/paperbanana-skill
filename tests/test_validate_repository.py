from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate-repository.py"


class ValidationTests(unittest.TestCase):
    def validate(self, files):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, content in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
            return subprocess.run([sys.executable, str(SCRIPT), str(root)], capture_output=True, text=True)

    def test_valid_frontmatter_and_local_reference(self):
        result = self.validate({"SKILL.md": "---\nname: demo\ndescription: A demo\n---\n[Guide](references/guide.md#start)\n", "references/guide.md": "# Start\n"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_invalid_yaml_is_rejected(self):
        result = self.validate({"SKILL.md": "---\nname: demo\ndescription: Demo\nargument-hint: [a|b] [text]\n---\n"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SKILL.md", result.stdout + result.stderr)

    def test_missing_relative_reference_is_rejected(self):
        result = self.validate({"README.md": "# Demo\n[Contract](references/missing.md)\n"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("references/missing.md", result.stdout + result.stderr)

    def test_missing_html_image_is_rejected(self):
        result = self.validate({"README.md": '<img src="examples/missing.webp" alt="demo"/>\n'})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("examples/missing.webp", result.stdout + result.stderr)

    def test_external_and_example_code_links_are_not_local_files(self):
        result = self.validate({"README.md": '# Demo\n[Docs](https://example.com/a)\n```md\n[placeholder](not-a-real-file.md)\n```\n'})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
