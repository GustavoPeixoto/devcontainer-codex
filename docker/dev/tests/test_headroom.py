"""Valida a integração sem credenciais reais ou chamadas de inferência.

Execute com /opt/headroom/bin/python docker/dev/tests/test_headroom.py.
O teste de proxy exige a porta 8787 livre, preferencialmente em outro container.
"""

import asyncio
import json
import os
from pathlib import Path
import signal
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest

import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import tomlkit


BIN_DIR = Path(os.environ.get(
    "HEADROOM_TEST_BIN",
    str(Path(__file__).resolve().parents[1] / "bin") if __file__ != "<stdin>" else "/usr/local/bin",
))
HEADROOM_CLI = os.environ.get("HEADROOM_CLI", "/usr/local/bin/headroom")


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.config_dir = Path(self.temporary.name)
        self.config_path = self.config_dir / "config.toml"
        self.env = {**os.environ, "CODEX_HOME": str(self.config_dir), "HEADROOM_PYTHON": sys.executable}
        self.env.pop("OPENAI_API_KEY", None)
        self.env.pop("HEADROOM_BEACON", None)

    def setup_headroom(self, *args, check=True):
        return subprocess.run(
            ["bash", str(BIN_DIR / "setup-codex-headroom"), *args],
            env=self.env, text=True, capture_output=True, check=check, timeout=30,
        )

    def config(self):
        return tomlkit.parse(self.config_path.read_text())

    def test_default_setup_automatically_enables_routing_and_is_idempotent(self):
        self.setup_headroom()
        original = self.config_path.read_bytes()
        self.setup_headroom()
        self.assertEqual(self.config_path.read_bytes(), original)
        config = self.config()
        self.assertEqual(config["model_provider"], "headroom")
        self.assertEqual(config["openai_base_url"], "http://127.0.0.1:8787/v1")
        self.assertTrue(config["model_providers"]["headroom"]["requires_openai_auth"])
        self.assertEqual((self.config_dir / "config.toml.before-headroom").read_bytes(), b"")
        self.assertEqual(config["mcp_servers"]["headroom"]["env"]["HEADROOM_BEACON"], "off")

    def test_enable_flag_remains_an_alias_of_default_setup(self):
        self.setup_headroom()
        configured = self.config_path.read_bytes()
        self.setup_headroom("--enable")
        self.assertEqual(self.config_path.read_bytes(), configured)

    def test_enable_disable_preserves_configuration_auth_hooks_and_history(self):
        original = '# Comentário do usuário\nmodel = "custom-model"\nmodel_provider = "other"\n'
        original += 'openai_base_url = "https://example.invalid/v1"\n'
        original += '[profiles.review]\nmodel_provider = "review-provider"\n'
        original += '[mcp_servers.other]\ncommand = "custom-mcp"\n'
        original += '[model_providers.headroom]\nname = "Existing provider"\nbase_url = "https://existing.invalid"\n'
        self.config_path.write_text(original)
        self.config_path.chmod(0o600)
        auth = self.config_dir / "auth.json"
        auth.write_text(json.dumps({"auth_mode": "chatgpt", "tokens": {"account_id": "test-account"}}))
        hooks = self.config_dir / "hooks.json"
        hooks.write_text('{"hooks":{"Stop":[]}}\n')
        with sqlite3.connect(self.config_dir / "state_5.sqlite") as db:
            db.execute("CREATE TABLE threads (id TEXT, model_provider TEXT)")
            db.execute("INSERT INTO threads VALUES ('existing', 'other')")
        protected = {p: p.read_bytes() for p in (auth, hooks, self.config_dir / "state_5.sqlite")}
        self.setup_headroom()
        enabled = self.config_path.read_bytes()
        self.setup_headroom()
        self.assertEqual(enabled, self.config_path.read_bytes())
        config = self.config()
        self.assertTrue(config["model_providers"]["headroom"]["requires_openai_auth"])
        self.assertNotIn("env_key", config["model_providers"]["headroom"])
        self.assertEqual(config["profiles"]["review"]["model_provider"], "review-provider")
        backup = self.config_dir / "config.toml.before-headroom"
        self.assertEqual(backup.read_text(), original)
        self.assertEqual(backup.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.config_path.stat().st_mode & 0o777, 0o600)
        config["model"] = "changed-after-enable"
        self.config_path.write_text(tomlkit.dumps(config))
        self.setup_headroom("--disable")
        restored = self.config()
        self.assertEqual(restored["model_provider"], "other")
        self.assertEqual(restored["openai_base_url"], "https://example.invalid/v1")
        self.assertEqual(restored["model_providers"]["headroom"]["base_url"], "https://existing.invalid")
        self.assertEqual(restored["model"], "changed-after-enable")
        self.assertIn("# Comentário do usuário", self.config_path.read_text())
        self.assertIn("headroom", restored["mcp_servers"])
        self.assertFalse(backup.exists())
        for path, content in protected.items():
            self.assertEqual(path.read_bytes(), content)
        self.setup_headroom()
        self.assertEqual(self.config()["model_provider"], "headroom")

    def test_api_key_auth_uses_environment_without_serializing_secret(self):
        self.env["OPENAI_API_KEY"] = "sk-test-not-a-real-key"
        self.setup_headroom()
        provider = self.config()["model_providers"]["headroom"]
        self.assertEqual(provider["env_key"], "OPENAI_API_KEY")
        self.assertNotIn("requires_openai_auth", provider)
        self.assertNotIn(self.env["OPENAI_API_KEY"], self.config_path.read_text())
        self.setup_headroom("--disable")
        self.assertNotIn("model_provider", self.config())
        self.assertNotIn("openai_base_url", self.config())
        self.assertNotIn("model_providers", self.config())

    def test_explicit_auth_allows_setup_before_login(self):
        self.setup_headroom("--auth", "chatgpt")
        self.assertTrue(self.config()["model_providers"]["headroom"]["requires_openai_auth"])
        self.setup_headroom("--auth", "api-key")
        self.assertEqual(self.config()["model_providers"]["headroom"]["env_key"], "OPENAI_API_KEY")
        self.assertNotIn("requires_openai_auth", self.config()["model_providers"]["headroom"])

    def test_fresh_volume_is_configured_before_login_and_can_be_restored(self):
        self.config_path.write_text('model = "custom-model"\ncli_auth_credentials_store = "file"\n')
        original = self.config_path.read_bytes()
        self.setup_headroom()
        self.assertEqual(self.config()["model_provider"], "headroom")
        self.assertEqual(self.config()["model"], "custom-model")
        self.assertTrue(self.config()["model_providers"]["headroom"]["requires_openai_auth"])
        self.assertEqual((self.config_dir / "config.toml.before-headroom").read_bytes(), original)
        self.assertFalse((self.config_dir / "auth.json").exists())
        self.setup_headroom("--disable")
        self.assertNotIn("model_provider", self.config())
        self.assertEqual(self.config()["model"], "custom-model")

    def test_invalid_config_and_http_mcp_conflict_are_not_overwritten(self):
        for content in ('[not valid', '[mcp_servers.headroom]\nurl = "https://mcp.invalid"\n'):
            with self.subTest(content=content):
                self.config_path.write_text(content)
                result = self.setup_headroom("--enable", "--auth", "chatgpt", check=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.config_path.read_text(), content)
                self.assertFalse((self.config_dir / "config.toml.before-headroom").exists())

    def test_disable_keeps_routing_changed_by_user(self):
        self.setup_headroom("--enable", "--auth", "chatgpt")
        config = self.config()
        config["model_provider"] = "changed-by-user"
        config["openai_base_url"] = "https://changed.invalid"
        config["model_providers"]["headroom"]["base_url"] = "https://changed-provider.invalid"
        self.config_path.write_text(tomlkit.dumps(config))
        self.setup_headroom("--disable")
        restored = self.config()
        self.assertEqual(restored["model_provider"], "changed-by-user")
        self.assertEqual(restored["openai_base_url"], "https://changed.invalid")
        self.assertEqual(restored["model_providers"]["headroom"]["base_url"], "https://changed-provider.invalid")

    def test_beacon_override_preserves_other_mcp_options(self):
        self.config_path.write_text('[mcp_servers.headroom]\nenabled = false\n[mcp_servers.headroom.env]\nCUSTOM = "kept"\n')
        self.env["HEADROOM_BEACON"] = "on"
        self.setup_headroom()
        server = self.config()["mcp_servers"]["headroom"]
        self.assertFalse(server["enabled"])
        self.assertEqual(server["env"]["CUSTOM"], "kept")
        self.assertEqual(server["env"]["HEADROOM_BEACON"], "on")

    def test_context_mode_can_be_configured_before_and_after_headroom(self):
        self.setup_headroom()
        subprocess.run(["bash", str(BIN_DIR / "setup-codex-context-mode")], env=self.env, check=True, capture_output=True)
        hooks = (self.config_dir / "hooks.json").read_bytes()
        self.setup_headroom("--enable", "--auth", "chatgpt")
        subprocess.run(["bash", str(BIN_DIR / "setup-codex-context-mode")], env=self.env, check=True, capture_output=True)
        config = self.config()
        self.assertEqual(config["model_provider"], "headroom")
        self.assertEqual(config["mcp_servers"]["context-mode"]["command"], "context-mode")
        self.assertIn("headroom", config["mcp_servers"])
        self.assertEqual((self.config_dir / "hooks.json").read_bytes(), hooks)


class ProxyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temporary.name)
        self.env = {
            **os.environ, "CODEX_HOME": str(self.config_dir), "HEADROOM_CLI": HEADROOM_CLI,
            "HEADROOM_BEACON": "off", "HEADROOM_STARTUP_TIMEOUT": "120",
            "HEADROOM_DISABLE_KOMPRESS": "1",
        }
        self.addCleanup(self.cleanup_proxy)

    def cleanup_proxy(self):
        pid_path = self.config_dir / "headroom/proxy.pid"
        if pid_path.exists():
            pid = int(pid_path.read_text())
            try:
                os.kill(pid, signal.SIGTERM)
                deadline = time.monotonic() + 5
                while time.monotonic() < deadline:
                    with socket.socket() as probe:
                        if probe.connect_ex(("127.0.0.1", 8787)) != 0:
                            break
                    time.sleep(0.1)
                else:
                    os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        self.temporary.cleanup()

    def start(self, **overrides):
        return subprocess.run(
            ["bash", str(BIN_DIR / "start-headroom-proxy")], env={**self.env, **overrides},
            text=True, capture_output=True, timeout=140,
        )

    def test_occupied_port_is_rejected_without_starting_proxy(self):
        with socket.socket() as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(("127.0.0.1", 8787))
            listener.listen()
            result = self.start()
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("porta 8787 ocupada", result.stderr)
            self.assertFalse((self.config_dir / "headroom/proxy.pid").exists())

    def test_invalid_timeout_and_process_exit_fail_cleanly(self):
        result = self.start(HEADROOM_STARTUP_TIMEOUT="invalid")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.config_dir / "headroom").exists())
        result = self.start(HEADROOM_CLI="/bin/false")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("processo encerrado", result.stderr)
        self.assertFalse((self.config_dir / "headroom/proxy.pid").exists())

    def test_concurrent_start_reuses_proxy_and_mcp_recovers_proxy_original(self):
        options = {**self.env, "HEADROOM_SAVINGS_PROFILE": "balanced", "HEADROOM_MODE": "token"}
        commands = [subprocess.Popen(
            ["bash", str(BIN_DIR / "start-headroom-proxy")], env=options,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        ) for _ in range(2)]
        for command in commands:
            stdout, stderr = command.communicate(timeout=140)
            log_path = self.config_dir / "headroom/proxy.log"
            log = log_path.read_text()[-3000:] if log_path.exists() else ""
            self.assertEqual(command.returncode, 0, stdout + stderr + log)
        pid_path = self.config_dir / "headroom/proxy.pid"
        pid = pid_path.read_text()
        result = self.start(**{"HEADROOM_SAVINGS_PROFILE": "balanced", "HEADROOM_MODE": "token"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(pid_path.read_text(), pid)
        self.assertIn("já está pronto", result.stdout)
        ready = httpx.get("http://127.0.0.1:8787/readyz").json()
        self.assertEqual(ready["service"], "headroom-proxy")
        self.assertTrue(ready["ready"])
        stats = httpx.get("http://127.0.0.1:8787/stats").json()
        self.assertEqual(stats["summary"]["mode"], "token")
        self.assertEqual(stats["config"]["savings_profile"], "balanced")
        # Dados aninhados exigem offload de linhas e geram um hash CCR recuperável.
        # Uma tabela homogênea pode ser comprimida sem perda e não precisa de hash.
        content = json.dumps([
            {"id": i, "data": {str(j): i * j for j in range(10)}, "status": "ok"}
            for i in range(500)
        ])
        response = httpx.post("http://127.0.0.1:8787/v1/compress", json={
            "model": "gpt-4o", "config": {"mode": "ccr"}, "messages": [
                {"role": "user", "content": "Find errors in these log entries."},
                {"role": "assistant", "content": None, "tool_calls": [
                    {"id": "logs", "type": "function", "function": {"name": "read_logs", "arguments": "{}"}},
                ]},
                {"role": "tool", "tool_call_id": "logs", "content": content},
            ],
        }, timeout=30)
        response.raise_for_status()
        compressed = response.json()
        self.assertLess(compressed["tokens_after"], compressed["tokens_before"])
        hashes = compressed.get("ccr_hashes", [])
        self.assertTrue(hashes, str(compressed)[-2000:])
        asyncio.run(self.check_mcp(hashes[0], content))

    async def check_mcp(self, proxy_hash, original):
        params = StdioServerParameters(
            command=HEADROOM_CLI,
            args=["mcp", "serve", "--proxy-url", "http://127.0.0.1:8787"], env=self.env,
        )
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                names = {tool.name for tool in (await session.list_tools()).tools}
                self.assertTrue({"headroom_compress", "headroom_retrieve", "headroom_stats"} <= names)
                retrieved = await session.call_tool("headroom_retrieve", {"hash": proxy_hash})
                self.assertFalse(retrieved.isError, str(retrieved))
                self.assert_original_recovered(retrieved, original)
                compressed = await session.call_tool("headroom_compress", {"content": original})
                self.assertFalse(compressed.isError)
                local_hash = json.loads(compressed.content[0].text)["hash"]
                retrieved = await session.call_tool("headroom_retrieve", {"hash": local_hash})
                self.assertFalse(retrieved.isError)
                self.assert_original_recovered(retrieved, original)

    def assert_original_recovered(self, retrieved, original):
        payload = json.loads(retrieved.content[0].text)
        self.assertTrue("original_content" in payload, f"Campos retornados: {list(payload)}")
        content = payload["original_content"]
        # O proxy pode devolver JSON serializado como string; compare os dados.
        for _ in range(3):
            if not isinstance(content, str):
                break
            content = json.loads(content)
        self.assertTrue(content == json.loads(original), "Conteúdo recuperado difere do original")


if __name__ == "__main__":
    unittest.main(verbosity=2)
