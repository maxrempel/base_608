#!/usr/bin/env python3
"""Reversible Codex backend switch: ChatGPT defaults <-> DeepSeek <-> Qwen.

Created 2026-08-05 by Codex for Max. The interactive Codex app on Pine was
switched from the ChatGPT backend to DeepSeek (2026-08-03), and is now being
tried on Alibaba's Qwen models (2026-08-05), currently the newest flagship
Qwen 3.8 Max. This tool flips the Codex config.toml between ChatGPT defaults
and the custom providers, and always keeps a backup, so every state can be
undone with one command:

    python switch_codex_backend.py chatgpt    # back to ChatGPT defaults
    python switch_codex_backend.py qwen       # Qwen 3.8 Max
    python switch_codex_backend.py qwen --model qwen3.7-plus  # Qwen variant
    python switch_codex_backend.py deepseek   # go back to DeepSeek
    python switch_codex_backend.py deepseek --model deepseek-v4-pro  # smart tier
    python switch_codex_backend.py status     # show which provider is active
    python switch_codex_backend.py disable-qwen  # turn Qwen off, key stays valid
    python switch_codex_backend.py enable-qwen   # bring Qwen back (catalog only)

`--model` accepts only variants that were verified working (see QWEN_MODELS and
DEEPSEEK_MODELS below), so stepping between Qwen versions, or from DeepSeek
Flash to DeepSeek Pro, is also one command and stays reversible.

What the tool changes (all inside ~/.codex, outside the git repository):
- config.toml: model, model_provider, model_auto_compact_token_limit,
  model_reasoning_effort, model_catalog_json, the API-key auth overrides, and
  the [model_providers.<name>] block (base_url, wire_api, bearer token).
- A timestamped backup of config.toml is written to ~/.codex/backups before
  every edit, and a per-provider snapshot to ~/.codex/backup-<provider>/.

The `chatgpt` action removes every backend override the tool writes, so the
app returns to stock defaults: the built-in `openai` provider with ChatGPT
OAuth sign-in and the app-managed default model. The model catalog
(~/.codex/models.json) keeps entries for the custom providers, so switching
back to DeepSeek or Qwen from ChatGPT defaults is still one command.

Safety: the API keys are read from the documented Nextcloud credential files
and written into config.toml only when that provider is activated. Nothing here
prints a key. If a key file is missing the switch fails closed.

While the disable marker `~/.codex/qwen.disabled` exists, `qwen` switches are
blocked unless `--force` is passed. Disabling never touches the Alibaba API
key; the key file stays valid for other uses.
"""

import argparse
import json
import os
import shutil
import sys
import tempfile
import tomllib
from datetime import datetime


CODEX_HOME = os.path.join(os.path.expanduser("~"), ".codex")
DEFAULT_CONFIG = os.path.join(CODEX_HOME, "config.toml")
DEFAULT_CATALOG = os.path.join(CODEX_HOME, "models.json")

SSH_CRED_DIR = r"C:\Users\maxre\Nextcloud\zSyncMain\ssh"

PROVIDERS = {
    "deepseek": {
        "label": "DeepSeek V4 Flash",
        "base_url": "https://api.deepseek.com/",
        "wire_api": "responses",
        "key_file": os.path.join(SSH_CRED_DIR, "deepseek_api_key_20260226.txt"),
        "model": "deepseek-v4-flash",
        "auto_compact_token_limit": 350000,
        "reasoning_effort": "high",
    },
    "qwen": {
        "label": "Qwen 3.8 Max (Alibaba DashScope)",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "wire_api": "responses",
        "key_file": os.path.join(SSH_CRED_DIR, "dashscope_beijing_api_key_20260329.txt"),
        "model": "qwen3.8-max",
        "auto_compact_token_limit": 350000,
        "reasoning_effort": "high",
    },
}

# Qwen variants verified working on the Alibaba DashScope account with the
# Beijing API key on 2026-08-05. The first one is the switch default.
QWEN_MODELS = {
    "qwen3.8-max": "Qwen 3.8 Max (newest flagship, default)",
    "qwen3.7-max": "Qwen 3.7 Max",
    "qwen3.7-plus": "Qwen 3.7 Plus (previous default)",
    "qwen3.7-flash": "Qwen 3.7 Flash",
    "qwen3.5-plus": "Qwen 3.5 Plus",
    "qwen3-max": "Qwen 3 Max",
    "qwen3-coder-480b-a35b-instruct": "Qwen3 Coder 480B",
}

# DeepSeek variants available to the interactive Codex backend. The plain
# `deepseek` action keeps the fast tier; Max steps up to the smart tier with
# `deepseek --model deepseek-v4-pro` (active choice 2026-08-05).
DEEPSEEK_MODELS = {
    "deepseek-v4-flash": "DeepSeek V4 Flash (fast default)",
    "deepseek-v4-pro": "DeepSeek V4 Pro (smart tier)",
}

DISABLED_MARKER = "qwen.disabled"


def marker_path():
    return os.path.join(CODEX_HOME, DISABLED_MARKER)


def read_key(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            key = handle.read().strip()
    except OSError as exc:
        raise RuntimeError(f"API key is unavailable at {path}") from exc
    if not key:
        raise RuntimeError(f"API key is empty at {path}")
    return key


def _fmt_value(value):
    if isinstance(value, int):
        return f"{value}"
    return f'"{value}"'


def rewrite_top_level(text, key, value):
    """Replace the first top-level `key = ...` line, inserting it if missing.

    ChatGPT-default configs omit the backend keys entirely, so switching to a
    custom provider from defaults must insert them instead of failing.
    """
    new_line = f"{key} = {_fmt_value(value)}"
    lines = text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(key + " =") or stripped.startswith(key + "="):
            lines[index] = new_line
            return "\n".join(lines) + "\n"
    return "\n".join([new_line] + lines) + "\n"


def remove_top_level_keys(text, keys):
    """Remove the given top-level `key = ...` lines from config text."""
    wanted = set(keys)
    lines = text.splitlines()
    kept = []
    removed = set()
    for line in lines:
        stripped = line.strip()
        hit = next(
            (
                key
                for key in wanted
                if stripped.startswith(key + " =")
                or stripped.startswith(key + "=")
            ),
            None,
        )
        if hit is not None:
            removed.add(hit)
        else:
            kept.append(line)
    cleaned = []
    for line in kept:
        if line.strip() == "" and cleaned and cleaned[-1].strip() == "":
            continue
        cleaned.append(line)
    return "\n".join(cleaned).rstrip("\n") + "\n", removed


def provider_block(name, spec):
    return "\n".join(
        [
            f"[model_providers.{name}]",
            f'name = "{name}"',
            f'base_url = "{spec["base_url"]}"',
            f'wire_api = "{spec["wire_api"]}"',
            f'experimental_bearer_token = "{spec["key"]}"',
        ]
    )


def upsert_provider_block(text, name, spec):
    block = provider_block(name, spec)
    lines = text.splitlines()
    marker = f"[model_providers.{name}]"
    start = None
    for index, line in enumerate(lines):
        if line.strip() == marker:
            start = index
            break
    if start is None:
        return text.rstrip("\n") + "\n\n" + block + "\n"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].lstrip().startswith("["):
            end = index
            break
    new_lines = lines[:start] + block.splitlines() + lines[end:]
    return "\n".join(new_lines) + "\n"


def remove_provider_block(text, name):
    """Remove the [model_providers.<name>] section from config text."""
    lines = text.splitlines()
    marker = f"[model_providers.{name}]"
    start = None
    for index, line in enumerate(lines):
        if line.strip() == marker:
            start = index
            break
    if start is None:
        return text
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].lstrip().startswith("["):
            end = index
            break
    new_lines = lines[:start] + lines[end:]
    cleaned = []
    for line in new_lines:
        if line.strip() == "" and cleaned and cleaned[-1].strip() == "":
            continue
        cleaned.append(line)
    return "\n".join(cleaned).rstrip("\n") + "\n"


def backup_catalog(catalog_path):
    backup_dir = os.path.join(CODEX_HOME, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = os.path.join(backup_dir, f"models.json.{stamp}")
    shutil.copy2(catalog_path, dest)
    return dest


def qwen_entries(catalog):
    return [
        m
        for m in catalog.get("models", [])
        if isinstance(m, dict)
        and str(m.get("slug") or "").lower().startswith("qwen")
    ]


def save_qwen_catalog_snapshot(entries):
    folder = os.path.join(CODEX_HOME, "backup-qwen")
    os.makedirs(folder, exist_ok=True)
    dest = os.path.join(folder, "models.qwen.json")
    with open(dest, "w", encoding="utf-8") as handle:
        json.dump({"models": entries}, handle, indent=2, ensure_ascii=False)
    return dest


def write_disable_marker():
    marker = marker_path()
    payload = {
        "disabled_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reason": (
            "Max asked to turn Qwen off in the interactive Codex app "
            "(2026-08-06). The Alibaba DashScope API key must stay valid "
            "for other uses and is not touched by this marker."
        ),
        "key_file": (
            "C:/Users/maxre/Nextcloud/zSyncMain/ssh/"
            "dashscope_beijing_api_key_20260329.txt"
        ),
        "restore": [
            "python switch_codex_backend.py enable-qwen",
            "python switch_codex_backend.py qwen",
        ],
    }
    with open(marker, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
    return marker


def backup_config(config_path):
    backup_dir = os.path.join(CODEX_HOME, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = os.path.join(backup_dir, f"config.toml.{stamp}")
    shutil.copy2(config_path, dest)
    return dest


def snapshot_provider(config_path, provider, spec, previous_provider):
    folder = os.path.join(CODEX_HOME, f"backup-{provider}")
    os.makedirs(folder, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    shutil.copy2(config_path, os.path.join(folder, "config.toml"))
    manifest = os.path.join(folder, "manifest.txt")
    with open(manifest, "w", encoding="utf-8") as handle:
        handle.write(
            "\n".join(
                [
                    "script_version=1.0.0",
                    f"switched_at={stamp}",
                    f"provider={provider}",
                    f"model={spec['model']}",
                    f"base_url={spec['base_url']}",
                    f"previous_provider={previous_provider or 'unknown'}",
                    "",
                ]
            )
        )


def load_config(config_path):
    with open(config_path, "rb") as handle:
        return tomllib.load(handle)


def verify(config_path, provider, catalog_path, spec):
    data = load_config(config_path)
    if data.get("model_provider") != provider:
        raise RuntimeError("verification failed: model_provider mismatch")
    if data.get("model") != spec["model"]:
        raise RuntimeError("verification failed: model mismatch")
    block = data.get("model_providers", {}).get(provider)
    if not block:
        raise RuntimeError("verification failed: provider block missing")
    if block.get("base_url") != spec["base_url"]:
        raise RuntimeError("verification failed: base_url mismatch")
    if block.get("wire_api") != spec["wire_api"]:
        raise RuntimeError("verification failed: wire_api mismatch")
    with open(catalog_path, "r", encoding="utf-8") as handle:
        catalog = json.load(handle)
    slugs = {m.get("slug") for m in catalog.get("models", [])}
    if spec["model"] not in slugs:
        raise RuntimeError(
            f"verification failed: model {spec['model']!r} is missing from "
            f"the model catalog"
        )


def switch(provider, config_path=None, catalog_path=None, model=None, force=False):
    if provider not in PROVIDERS:
        raise RuntimeError(
            f"unknown provider {provider!r}; choose from {sorted(PROVIDERS)}"
        )
    if model is not None:
        if provider not in ("qwen", "deepseek"):
            raise RuntimeError(
                f"--model is only valid for the qwen and deepseek providers, "
                f"not {provider!r}"
            )
        allowed = QWEN_MODELS if provider == "qwen" else DEEPSEEK_MODELS
        if model not in allowed:
            display = {"qwen": "Qwen", "deepseek": "DeepSeek"}.get(
                provider, provider
            )
            raise RuntimeError(
                f"unknown {display} variant {model!r}; "
                f"choose from {sorted(allowed)}"
            )
    config_path = config_path or DEFAULT_CONFIG
    catalog_path = catalog_path or DEFAULT_CATALOG
    explicit_model = model
    model = model or PROVIDERS[provider]["model"]
    spec = {**PROVIDERS[provider], "model": model}
    if provider == "qwen":
        spec["label"] = QWEN_MODELS.get(model, spec["label"])
    else:
        spec["label"] = DEEPSEEK_MODELS.get(model, spec["label"])

    if provider == "qwen":
        marker = marker_path()
        if os.path.isfile(marker) and not force:
            raise RuntimeError(
                "Qwen is disabled on this machine (marker file exists at "
                f"{marker}). Re-enable with "
                "'switch_codex_backend.py enable-qwen', then "
                "'switch_codex_backend.py qwen'. To override once, pass "
                "--force."
            )

    key = read_key(spec["key_file"])

    if not os.path.isfile(config_path):
        raise RuntimeError(f"config.toml not found at {config_path}")
    if not os.path.isfile(catalog_path):
        raise RuntimeError(f"model catalog not found at {catalog_path}")

    with open(catalog_path, "r", encoding="utf-8") as handle:
        catalog = json.load(handle)
    slugs = {m.get("slug") for m in catalog.get("models", [])}
    if spec["model"] not in slugs:
        raise RuntimeError(
            f"model {spec['model']!r} is missing from the model catalog; "
            f"nothing was changed"
        )

    current = load_config(config_path)
    previous = current.get("model_provider")
    previous_model = current.get("model")
    # Always back up before any edit, including a same-provider model change
    # or a token refresh, so every prior state stays restorable.
    backup_path = backup_config(config_path)
    print(f"Backup written to {backup_path}")
    with open(config_path, "r", encoding="utf-8") as handle:
        text = handle.read()

    text = rewrite_top_level(text, "model", spec["model"])
    text = rewrite_top_level(text, "model_provider", provider)
    text = rewrite_top_level(
        text, "model_auto_compact_token_limit", spec["auto_compact_token_limit"]
    )
    text = rewrite_top_level(
        text, "model_reasoning_effort", spec["reasoning_effort"]
    )
    # Custom models live in the local catalog, and the API-key auth overrides
    # keep the app from falling back to ChatGPT OAuth while a custom provider
    # is active. ChatGPT defaults remove all of these.
    for top_key, top_value in (
        ("model_catalog_json", catalog_path.replace("\\", "/")),
        ("preferred_auth_method", "apikey"),
        ("forced_login_method", "api"),
    ):
        text = rewrite_top_level(text, top_key, top_value)
    text = upsert_provider_block(text, provider, {**spec, "key": key})

    fd, tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(config_path), suffix=".tmp"
    )
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.replace(tmp_path, config_path)

    snapshot_provider(config_path, provider, spec, previous)
    verify(config_path, provider, catalog_path, spec)
    if (
        previous in PROVIDERS
        and previous_model
        and previous_model != spec["model"]
    ):
        revert_cmd = previous
        if previous_model != PROVIDERS[previous]["model"]:
            revert_cmd += f" --model {previous_model}"
    else:
        revert_cmd = "deepseek" if provider != "deepseek" else "qwen"
    print(
        f"OK: Codex backend is now {provider} ({spec['label']}), model "
        f"{spec['model']}. Revert with: python "
        f"{os.path.abspath(__file__)} "
        f"{revert_cmd}"
    )


def disable_qwen(config_path=None, catalog_path=None):
    """Turn Qwen off in the interactive Codex app; the API key stays valid."""
    config_path = config_path or DEFAULT_CONFIG
    catalog_path = catalog_path or DEFAULT_CATALOG
    for path, label in ((config_path, "config"), (catalog_path, "catalog")):
        if not os.path.isfile(path):
            raise RuntimeError(f"{label} not found at {path}")
    config_backup = backup_config(config_path)
    catalog_backup = backup_catalog(catalog_path)

    with open(config_path, "r", encoding="utf-8") as handle:
        text = handle.read()
    text = remove_provider_block(text, "qwen")
    fd, tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(config_path), suffix=".tmp"
    )
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.replace(tmp_path, config_path)

    with open(catalog_path, "r", encoding="utf-8") as handle:
        catalog = json.load(handle)
    entries = qwen_entries(catalog)
    catalog["models"] = [m for m in catalog["models"] if m not in entries]
    snapshot = save_qwen_catalog_snapshot(entries)
    fd, tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(catalog_path), suffix=".tmp"
    )
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(catalog, handle, indent=2, ensure_ascii=False)
    os.replace(tmp_path, catalog_path)

    marker = write_disable_marker()

    data = load_config(config_path)
    if "qwen" in data.get("model_providers", {}):
        raise RuntimeError(
            "verification failed: qwen provider block still present"
        )
    with open(catalog_path, "r", encoding="utf-8") as handle:
        catalog2 = json.load(handle)
    if qwen_entries(catalog2):
        raise RuntimeError("verification failed: qwen models still in catalog")
    if not os.path.isfile(marker):
        raise RuntimeError("verification failed: disable marker not written")

    print("OK: Qwen is disabled for the interactive Codex app.")
    print(f"  config backup : {config_backup}")
    print(f"  catalog backup: {catalog_backup}")
    print(f"  qwen entries  : {snapshot} ({len(entries)} models)")
    print(f"  marker        : {marker}")
    print("Re-enable later with: python switch_codex_backend.py enable-qwen")


def enable_qwen(config_path=None, catalog_path=None):
    """Restore Qwen catalog entries and remove the disable marker."""
    config_path = config_path or DEFAULT_CONFIG
    catalog_path = catalog_path or DEFAULT_CATALOG
    marker = marker_path()
    if not os.path.isfile(marker):
        raise RuntimeError("Qwen is not disabled; no marker file found")
    snapshot = os.path.join(CODEX_HOME, "backup-qwen", "models.qwen.json")
    if not os.path.isfile(snapshot):
        raise RuntimeError(
            f"cannot restore Qwen catalog entries: missing {snapshot}"
        )
    with open(snapshot, "r", encoding="utf-8") as handle:
        saved = json.load(handle)
    with open(catalog_path, "r", encoding="utf-8") as handle:
        catalog = json.load(handle)
    existing = {
        m.get("slug")
        for m in catalog.get("models", [])
        if isinstance(m, dict)
    }
    for m in saved.get("models", []):
        if m.get("slug") not in existing:
            catalog.setdefault("models", []).append(m)
    fd, tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(catalog_path), suffix=".tmp"
    )
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(catalog, handle, indent=2, ensure_ascii=False)
    os.replace(tmp_path, catalog_path)
    os.remove(marker)
    print("OK: Qwen is available again in the model catalog.")
    print("Activate it with: python switch_codex_backend.py qwen")


CHATGPT_DEFAULT_KEYS_TO_REMOVE = (
    "model",
    "model_provider",
    "model_auto_compact_token_limit",
    "model_reasoning_effort",
    "preferred_auth_method",
    "forced_login_method",
    "model_catalog_json",
)


def restore_chatgpt(config_path=None, catalog_path=None):
    """Restore the built-in ChatGPT defaults in the interactive Codex app.

    Removes every backend override the switch tool ever writes, so the app
    goes back to stock defaults: the built-in `openai` provider with ChatGPT
    OAuth sign-in and the app-managed default model (gpt-5.6-sol as of
    2026-08-07). Custom provider blocks are removed too; the API key files in
    Nextcloud are never touched.
    """
    config_path = config_path or DEFAULT_CONFIG
    if not os.path.isfile(config_path):
        raise RuntimeError(f"config.toml not found at {config_path}")
    backup_path = backup_config(config_path)

    with open(config_path, "r", encoding="utf-8") as handle:
        text = handle.read()

    text, removed = remove_top_level_keys(text, CHATGPT_DEFAULT_KEYS_TO_REMOVE)
    for name in list(load_config(config_path).get("model_providers", {})):
        text = remove_provider_block(text, name)

    fd, tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(config_path), suffix=".tmp"
    )
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.replace(tmp_path, config_path)

    data = load_config(config_path)
    if "model_provider" in data:
        raise RuntimeError("verification failed: model_provider still present")
    if "model" in data:
        raise RuntimeError("verification failed: model override still present")
    if data.get("model_providers"):
        raise RuntimeError(
            "verification failed: custom provider blocks still present"
        )
    for key in (
        "preferred_auth_method",
        "forced_login_method",
        "model_catalog_json",
        "model_reasoning_effort",
        "model_auto_compact_token_limit",
    ):
        if key in data:
            raise RuntimeError(f"verification failed: {key} still present")

    snapshot_provider(
        config_path,
        "chatgpt",
        {
            "model": "app default (gpt-5.6-sol)",
            "base_url": "built-in openai provider",
        },
        data.get("model_provider"),
    )
    print(f"Backup written to {backup_path}")
    print(
        "OK: Codex backend is back on ChatGPT defaults (built-in openai "
        "provider, app-managed model). Restart the Codex app for new tasks."
    )


def status(config_path=None, catalog_path=None):
    config_path = config_path or DEFAULT_CONFIG
    catalog_path = catalog_path or DEFAULT_CATALOG
    data = load_config(config_path)
    provider = data.get("model_provider")
    print(f"active provider : {provider}")
    print(f"active model    : {data.get('model')}")
    print(f"reasoning effort: {data.get('model_reasoning_effort')}")
    print(f"auto compact    : {data.get('model_auto_compact_token_limit')}")
    print(f"config file     : {config_path}")
    print("configured providers:")
    for name in sorted(data.get("model_providers", {})):
        block = data["model_providers"][name]
        key_ok = os.path.isfile(PROVIDERS.get(name, {}).get("key_file", ""))
        print(
            f"  - {name}: base_url={block.get('base_url')} "
            f"wire_api={block.get('wire_api')} key_file_present={key_ok}"
        )
    with open(catalog_path, "r", encoding="utf-8") as handle:
        catalog = json.load(handle)
    slugs = [m.get("slug") for m in catalog.get("models", [])]
    print("catalog models  : " + ", ".join(slugs))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        nargs="?",
        default="status",
        help=(
            "chatgpt | qwen | deepseek | disable-qwen | enable-qwen | status"
        ),
    )
    parser.add_argument(
        "--model",
        default=None,
        help="model variant to activate (see QWEN_MODELS / DEEPSEEK_MODELS)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="override the Qwen disable marker for one switch",
    )
    parser.add_argument("--config", default=None, help="override config.toml path")
    parser.add_argument("--catalog", default=None, help="override models.json path")
    args = parser.parse_args()

    try:
        if args.action == "status":
            status(args.config, args.catalog)
        elif args.action == "chatgpt":
            restore_chatgpt(args.config, args.catalog)
        elif args.action == "disable-qwen":
            disable_qwen(args.config, args.catalog)
        elif args.action == "enable-qwen":
            enable_qwen(args.config, args.catalog)
        else:
            switch(
                args.action,
                args.config,
                args.catalog,
                args.model,
                force=args.force,
            )
    except Exception as exc:
        print(f"switch_codex_backend FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
