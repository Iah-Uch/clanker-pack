"""Tests for the safety-pack hooks. Run: python3 -m unittest plugins/safety-pack/hooks/test_hooks.py

Fake secrets are built at run time so that no secret scanner flags this file.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script: str, payload: dict, env: dict | None = None):
    result = subprocess.run(
        [sys.executable, os.path.join(HERE, script)],
        input=json.dumps(payload), capture_output=True, text=True,
        env={**os.environ, **(env or {})}, timeout=10,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)["hookSpecificOutput"] if result.stdout.strip() else None


def bash(command: str):
    return run("guard_bash.py", {"tool_name": "Bash", "tool_input": {"command": command}})


def kind(out):
    return out["permissionDecision"] if out else None


class GuardBash(unittest.TestCase):
    def test_denies_home_wipe(self):
        self.assertEqual(kind(bash("rm -rf ~")), "deny")
        self.assertEqual(kind(bash("rm -rf /")), "deny")
        self.assertEqual(kind(bash('rm -rf "$HOME"')), "deny")
        self.assertEqual(kind(bash("cd x && rm -fr /*")), "deny")

    def test_denies_disk_and_fork_bomb(self):
        self.assertEqual(kind(bash("dd if=/dev/zero of=/dev/sda")), "deny")
        self.assertEqual(kind(bash(":(){ :|:& };:")), "deny")

    def test_asks_before_rm_rf_of_real_dirs(self):
        self.assertEqual(kind(bash("rm -rf src")), "ask")

    def test_allows_rm_rf_of_build_output(self):
        self.assertIsNone(bash("rm -rf node_modules dist"))

    def test_allows_plain_rm(self):
        self.assertIsNone(bash("rm file.txt"))

    def test_force_push(self):
        self.assertEqual(kind(bash("git push --force origin feat/x")), "ask")
        self.assertEqual(kind(bash("git push -f origin main")), "deny")
        self.assertIsNone(bash("git push origin feat/x"))

    def test_git_destroyers_ask(self):
        for command in ("git reset --hard HEAD~1", "git clean -fd", "git checkout .", "git branch -D old"):
            self.assertEqual(kind(bash(command)), "ask", command)

    def test_sql_destroyers_ask(self):
        self.assertEqual(kind(bash('psql -c "DROP TABLE users"')), "ask")
        self.assertEqual(kind(bash('psql -c "DELETE FROM users;"')), "ask")
        self.assertIsNone(bash('psql -c "DELETE FROM users WHERE id = 3"'))

    def test_normal_commands_pass(self):
        for command in ("ls -la", "git status", "npm test", "git push", "git commit -m 'fix: x'"):
            self.assertIsNone(bash(command), command)

    def test_bad_input_does_not_crash(self):
        result = subprocess.run([sys.executable, os.path.join(HERE, "guard_bash.py")],
                                input="not json", capture_output=True, text=True)
        self.assertEqual((result.returncode, result.stdout), (0, ""))


class SecretScan(unittest.TestCase):
    def scan(self, content: str, path: str = "src/app.ts", key: str = "content"):
        return run("secret_scan.py", {"tool_name": "Write", "tool_input": {"file_path": path, key: content}})

    def test_denies_real_shaped_keys(self):
        samples = {
            "aws": "const k = '" + "AKIA" + "A" * 16 + "'",
            "github": "t = " + "ghp_" + "a" * 36,
            "stripe": "k = '" + "sk_live_" + "a" * 24 + "'",
            "private": "-----BEGIN " + "RSA PRIVATE KEY-----",
        }
        for name, text in samples.items():
            self.assertEqual(kind(self.scan(text)), "deny", name)

    def test_denies_hardcoded_credential(self):
        self.assertEqual(kind(self.scan('const apiKey = "' + "q7Zx" * 6 + '"')), "deny")

    def test_reason_does_not_echo_secret(self):
        out = self.scan("t = " + "ghp_" + "b" * 36)
        self.assertNotIn("b" * 36, out["permissionDecisionReason"])
        self.assertIn("line 1", out["permissionDecisionReason"])

    def test_allows_env_reads_and_placeholders(self):
        self.assertIsNone(self.scan("const apiKey = process.env.API_KEY"))
        self.assertIsNone(self.scan('API_KEY = "your_api_key_goes_here_please"'))

    def test_allows_example_files_and_marker(self):
        self.assertIsNone(self.scan("k = 'AKIA" + "A" * 16 + "'", path=".env.example"))
        self.assertIsNone(self.scan("# secret-scan: allow\nk = 'AKIA" + "A" * 16 + "'"))

    def test_checks_edit_new_string(self):
        self.assertEqual(kind(self.scan("t = ghp_" + "c" * 36, key="new_string")), "deny")


class Watchdog(unittest.TestCase):
    def transcript(self, tokens: int) -> str:
        handle = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False)
        handle.write(json.dumps({"type": "user", "message": {"content": "hi"}}) + "\n")
        handle.write(json.dumps({"type": "assistant", "message": {"usage": {
            "input_tokens": 2, "cache_read_input_tokens": tokens, "cache_creation_input_tokens": 0}}}) + "\n")
        handle.close()
        self.addCleanup(os.unlink, handle.name)
        return handle.name

    def prompt(self, tokens: int, session: str):
        marker = os.path.join(tempfile.gettempdir(), f"clanker-watchdog-{session}-0")
        if os.path.exists(marker):
            os.unlink(marker)
        self.addCleanup(lambda: os.path.exists(marker) and os.unlink(marker))
        return run("context_watchdog.py", {"transcript_path": self.transcript(tokens), "session_id": session})

    def test_silent_below_threshold(self):
        self.assertIsNone(self.prompt(100_000, "t-low"))

    def test_warns_above_threshold_once(self):
        first = self.prompt(300_000, "t-high")
        self.assertIn("300k tokens", first["additionalContext"])
        again = run("context_watchdog.py", {"transcript_path": self.transcript(300_000), "session_id": "t-high"})
        self.assertIsNone(again)

    def test_threshold_from_env(self):
        out = run("context_watchdog.py",
                  {"transcript_path": self.transcript(60_000), "session_id": "t-env"},
                  env={"CLANKER_WATCHDOG_TOKENS": "50000"})
        self.addCleanup(lambda: os.path.exists(m := os.path.join(tempfile.gettempdir(), "clanker-watchdog-t-env-0")) and os.unlink(m))
        self.assertIsNotNone(out)


if __name__ == "__main__":
    unittest.main()
