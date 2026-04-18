from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from mainpy.cleaner import cleanup_junk, scan_junk
from mainpy.logger import get_logger


class CleanerTests(unittest.TestCase):
    def test_scan_junk_finds_matching_extensions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "keep.txt").write_text("ok", encoding="utf-8")
            (root / "delete.tmp").write_text("tmp", encoding="utf-8")
            (root / "archive.bak").write_text("bak", encoding="utf-8")

            matches = scan_junk(root, [".tmp", ".bak"])

            self.assertEqual(
                [path.name for path in matches],
                ["archive.bak", "delete.tmp"],
            )

    def test_cleanup_junk_deletes_files_and_counts_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            removable = root / "cache.tmp"
            removable.write_text("hello", encoding="utf-8")

            result = cleanup_junk(root, [".tmp"], logger=get_logger())

            self.assertEqual(result["deleted_count"], 1)
            self.assertEqual(result["freed_bytes"], 5)
            self.assertFalse(removable.exists())


if __name__ == "__main__":
    unittest.main()
