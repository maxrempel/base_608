import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "mdindex_sync.py"
SPEC = importlib.util.spec_from_file_location("mdindex_sync", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class MdindexSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.source.mkdir()
        self.registry = self.root / "folder_registry.txt"
        self.registry.write_text(f"{self.source}|5\n", encoding="utf-8")
        self.config = MODULE.Config(
            folder_registry=self.registry,
            mdindex_file=self.root / "mdindex.md",
            memex_dir=self.root / "memex" / "from_tomemex",
            log_file=self.root / "mdindex.log",
            hash_cache=self.root / "hashes.txt",
            health_file=self.root / "health.json",
            lock_file=self.root / "mdindex.lock",
        )

    def tearDown(self):
        self.temp.cleanup()

    def write_docs(self, count):
        for number in range(count):
            (self.source / f"doc_{number:02d}_tomemex.md").write_text(
                f"# Document {number}\n", encoding="utf-8"
            )

    def test_healthy_sync_builds_index_and_staging(self):
        self.write_docs(3)
        event = MODULE.run_once(self.config)
        self.assertTrue(event["healthy"])
        self.assertEqual(event["copied"], 3)
        self.assertIn("doc 00", self.config.mdindex_file.read_text(encoding="utf-8"))
        self.assertEqual(len(list(self.config.memex_dir.glob("local_*.md"))), 3)
        self.assertIn('"healthy": true', self.config.health_file.read_text(encoding="utf-8"))

    def test_scan_collapse_preserves_last_healthy_state(self):
        self.write_docs(25)
        first = MODULE.run_once(self.config)
        self.assertTrue(first["healthy"])
        old_index = self.config.mdindex_file.read_bytes()
        old_cache = self.config.hash_cache.read_bytes()
        old_staged = sorted(path.name for path in self.config.memex_dir.glob("local_*.md"))

        for path in list(self.source.glob("*_tomemex.md"))[:10]:
            path.unlink()
        second = MODULE.run_once(self.config)

        self.assertFalse(second["healthy"])
        self.assertIn("scan collapse", " ".join(second["failures"]))
        self.assertEqual(self.config.mdindex_file.read_bytes(), old_index)
        self.assertEqual(self.config.hash_cache.read_bytes(), old_cache)
        self.assertEqual(
            sorted(path.name for path in self.config.memex_dir.glob("local_*.md")),
            old_staged,
        )
        self.assertIn('"healthy": false', self.config.health_file.read_text(encoding="utf-8"))

    def test_small_real_removal_is_quarantined_not_deleted(self):
        self.write_docs(25)
        MODULE.run_once(self.config)
        removed = self.source / "doc_00_tomemex.md"
        removed.unlink()

        event = MODULE.run_once(self.config)

        self.assertTrue(event["healthy"])
        self.assertEqual(event["quarantined"], 1)
        quarantined = list(self.config.quarantine_dir.rglob("local_*doc_00_tomemex.md"))
        self.assertEqual(len(quarantined), 1)

    def test_instance_lock_rejects_duplicate(self):
        first = MODULE.acquire_instance_lock(self.config.lock_file)
        self.assertIsNotNone(first)
        try:
            second = MODULE.acquire_instance_lock(self.config.lock_file)
            self.assertIsNone(second)
        finally:
            MODULE.release_instance_lock(first)


if __name__ == "__main__":
    unittest.main()
