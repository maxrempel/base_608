import json
import os
import tempfile
import unittest

import switch_codex_backend as sw


SAMPLE_CONFIG = """\
model = "deepseek-v4-flash"
approval_policy = "never"
model_auto_compact_token_limit = 350000
model_reasoning_effort = "high"
model_provider = "deepseek"

[model_providers.deepseek]
name = "deepseek"
base_url = "https://api.deepseek.com/"
wire_api = "responses"
experimental_bearer_token = "old-deepseek-key"
"""


class SwitchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        self.config = os.path.join(self.root, "config.toml")
        self.catalog = os.path.join(self.root, "models.json")
        self.keys = {}
        for name, spec in sw.PROVIDERS.items():
            key_path = os.path.join(self.root, f"{name}_key.txt")
            with open(key_path, "w", encoding="utf-8") as handle:
                handle.write(f"sk-{name}-test-key\n")
            self.keys[name] = key_path
            spec["key_file"] = key_path
        with open(self.config, "w", encoding="utf-8") as handle:
            handle.write(SAMPLE_CONFIG)
        catalog = {
            "models": [
                {"slug": "deepseek-v4-flash"},
                {"slug": "deepseek-v4-pro"},
                {"slug": "qwen3.8-max"},
                {"slug": "qwen3.7-plus"},
            ]
        }
        with open(self.catalog, "w", encoding="utf-8") as handle:
            json.dump(catalog, handle)
        self.old_home = sw.CODEX_HOME
        sw.CODEX_HOME = os.path.join(self.root, "codex_home")

    def tearDown(self):
        sw.CODEX_HOME = self.old_home
        for name, spec in sw.PROVIDERS.items():
            spec["key_file"] = os.path.join(
                sw.SSH_CRED_DIR,
                {
                    "deepseek": "deepseek_api_key_20260226.txt",
                    "qwen": "dashscope_beijing_api_key_20260329.txt",
                }[name],
            )
        self.tmp.cleanup()

    def test_switch_to_qwen(self):
        sw.switch("qwen", self.config, self.catalog)
        data = sw.load_config(self.config)
        self.assertEqual(data["model_provider"], "qwen")
        self.assertEqual(data["model"], "qwen3.8-max")
        self.assertEqual(data["model_auto_compact_token_limit"], 350000)
        block = data["model_providers"]["qwen"]
        self.assertEqual(
            block["base_url"], "https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.assertEqual(block["wire_api"], "responses")
        self.assertEqual(block["experimental_bearer_token"], "sk-qwen-test-key")
        # DeepSeek block must survive so the switch is reversible.
        self.assertIn("deepseek", data["model_providers"])

    def test_switch_to_qwen_variant(self):
        sw.switch("qwen", self.config, self.catalog, model="qwen3.7-plus")
        data = sw.load_config(self.config)
        self.assertEqual(data["model_provider"], "qwen")
        self.assertEqual(data["model"], "qwen3.7-plus")
        self.assertEqual(
            data["model_providers"]["qwen"]["experimental_bearer_token"],
            "sk-qwen-test-key",
        )

    def test_unknown_qwen_variant_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, "unknown Qwen variant"):
            sw.switch("qwen", self.config, self.catalog, model="qwen2.0-bogus")

    def test_switch_back_to_deepseek(self):
        sw.switch("qwen", self.config, self.catalog)
        sw.switch("deepseek", self.config, self.catalog)
        data = sw.load_config(self.config)
        self.assertEqual(data["model_provider"], "deepseek")
        self.assertEqual(data["model"], "deepseek-v4-flash")
        self.assertEqual(
            data["model_providers"]["deepseek"]["experimental_bearer_token"],
            "sk-deepseek-test-key",
        )

    def test_switch_to_deepseek_pro_variant(self):
        sw.switch("qwen", self.config, self.catalog)
        sw.switch("deepseek", self.config, self.catalog, model="deepseek-v4-pro")
        data = sw.load_config(self.config)
        self.assertEqual(data["model_provider"], "deepseek")
        self.assertEqual(data["model"], "deepseek-v4-pro")
        self.assertEqual(
            data["model_providers"]["deepseek"]["experimental_bearer_token"],
            "sk-deepseek-test-key",
        )
        # Qwen block must survive so the switch is reversible.
        self.assertIn("qwen", data["model_providers"])

    def test_unknown_deepseek_variant_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, "unknown DeepSeek variant"):
            sw.switch("deepseek", self.config, self.catalog, model="deepseek-v3-bogus")

    def test_missing_key_fails_closed(self):
        sw.PROVIDERS["qwen"]["key_file"] = os.path.join(self.root, "missing.txt")
        with self.assertRaisesRegex(RuntimeError, "unavailable"):
            sw.switch("qwen", self.config, self.catalog)

    def test_backups_created(self):
        sw.switch("qwen", self.config, self.catalog)
        backups = os.listdir(os.path.join(sw.CODEX_HOME, "backups"))
        self.assertEqual(len(backups), 1)
        snapshot = os.path.join(sw.CODEX_HOME, "backup-qwen", "config.toml")
        self.assertTrue(os.path.isfile(snapshot))

    def test_disable_qwen_blocks_switch(self):
        sw.disable_qwen(self.config, self.catalog)
        data = sw.load_config(self.config)
        self.assertNotIn("qwen", data["model_providers"])
        with self.assertRaisesRegex(RuntimeError, "Qwen is disabled"):
            sw.switch("qwen", self.config, self.catalog)

    def test_enable_qwen_restores_switch(self):
        sw.disable_qwen(self.config, self.catalog)
        sw.enable_qwen(self.config, self.catalog)
        sw.switch("qwen", self.config, self.catalog)
        data = sw.load_config(self.config)
        self.assertEqual(data["model_provider"], "qwen")


if __name__ == "__main__":
    unittest.main()
