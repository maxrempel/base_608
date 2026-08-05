# Adviser note - milestone 1 (~121K tokens)
# session: 20260618_fervent_ptolemy_f16b4e_f0883cf5
# written: 2026-06-18 14:00:58 by deepseek-v4-pro

TO MAX: The Assistant is writing your AstolfoDebian password and SSH host details into a plaintext file in Nextcloud (`shared_logins_frequent.txt`). That file now contains a cleartext password synced to who-knows-where. You should decide whether you want credentials scattered outside Bitwarden. The private key you pasted is also now in this session transcript - consider rotating it afterward.

TO ASSISTANT: Stop writing passwords to plaintext files, full stop. The user, password, and host details for asto did not belong in `shared_logins_frequent.txt`. Bitwarden exists for a reason. If you need to cache a non-secret fact (hostname, fingerprint, user), that's fine - but passwords and keys stay in the secrets manager, never on disk. Also, you're 11 turns in and haven't confirmed Tailscale is joined or used the key Max just gave you. Prioritize: check Tailscale status, add the key to ssh-agent (or a temp keyfile with 0600 perms), and connect. Skip the credential-dumping habit.
