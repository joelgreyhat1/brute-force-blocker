# Brute-Force Blocker

A lightweight intrusion prevention tool that watches a log file for repeated failed login attempts and automatically blocks attacking IPs using real Windows Firewall rules — a minimal, purpose-built version of what fail2ban does on Linux servers.

## The Idea

After building a [brute-force login tester](https://github.com/joelgreyhat1/brute-force-tester) that cracked VulnBank's login in under a second, my next question was: what would actually stop that? Rate-limiting and account lockouts help at the app level, but there's a lower layer worth thinking about — blocking the attacking IP at the firewall before the request even reaches the application. That's what this tool does.

The log-watching approach here is the same pattern fail2ban uses in production. Tail a log file, parse failure lines as they arrive, count failures per IP within a sliding time window, and fire a block when the threshold is crossed. Building it from scratch made the design decisions in real tools like fail2ban make a lot more sense — particularly why the time window matters more than a raw failure count, and why cleanup on exit isn't optional.

## What It Does

- Tails a log file in real time, watching for `FAILED_LOGIN` entries
- Tracks failure counts per IP within a configurable sliding time window
- Blocks an IP via a real Windows Firewall inbound rule the moment it crosses the threshold
- Automatically unbans IPs after a configurable ban duration
- Cleans up all firewall rules it created when stopped — no orphaned rules left behind
- Comes with a `simulate_attacks.py` script that generates realistic failed login log entries so you can test without needing a live target

## How It Pairs with the Brute-Force Tester

This tool is the direct defensive counterpart to my [brute-force login tester](https://github.com/joelgreyhat1/brute-force-tester). The tester shows how fast a weak password falls when there's no protection. This blocker shows what that protection looks like — and demonstrates that it works, not just that it should.

## Requirements

- Python 3 (standard library only — no external dependencies)
- **Must be run as Administrator** — creating Windows Firewall rules via `netsh` requires elevated privileges

## Usage

```bash
git clone https://github.com/joelgreyhat1/brute-force-blocker.git
cd brute-force-blocker
```

Start the blocker (as Administrator):
```bash
python main.py --threshold 5 --window 60 --ban-duration 300
```

In a second terminal, simulate an attack:
```bash
python simulate_attacks.py
```

Check Windows Defender Firewall → Advanced Settings → Inbound Rules for `BruteForceBlocker_` entries confirming the blocks landed. Hit Ctrl+C to stop the blocker — it removes all rules it created before exiting.

## Configuration

| Flag | Default | What it controls |
|---|---|---|
| `--log` | `auth.log` | Log file to watch |
| `--threshold` | `5` | Failures before blocking |
| `--window` | `60` | Time window in seconds |
| `--ban-duration` | `300` | Seconds before auto-unban |

## Example Output

```
Watching auth.log for brute-force attempts...
  Threshold   : 5 failures in 60s
  Ban duration: 300s

[SIMULATED] Failed login from 192.168.1.50
[SIMULATED] Failed login from 192.168.1.50
...
[BLOCKED] 192.168.1.50 — 10 failures in 60s
[FIREWALL] Rule added: block inbound from 192.168.1.50
[BLOCKED] 192.168.1.75 — 10 failures in 60s
[FIREWALL] Rule added: block inbound from 192.168.1.75

^C
Stopping blocker...
[FIREWALL] All blocker rules cleaned up.
Done.
```

## What I Learned

- Why the sliding time window matters more than a raw failure count — a single IP failing 5 times over 3 days is normal noise; the same 5 failures in 10 seconds is a clear attack signal
- That cleanup isn't optional in a tool like this — leaving orphaned firewall rules behind after testing breaks other things, and prefixing every rule name made reliable cleanup straightforward
- How much the design of fail2ban made more sense after building a simpler version of it from scratch, rather than just reading its documentation

## License

MIT — for authorized use on systems you own or manage.