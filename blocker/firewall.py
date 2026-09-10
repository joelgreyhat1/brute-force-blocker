import subprocess

RULE_PREFIX = "BruteForceBlocker"

def block_ip(ip):
    rule_name = f"{RULE_PREFIX}_{ip}"
    result = subprocess.run(
        [
            "netsh", "advfirewall", "firewall", "add", "rule",
            f"name={rule_name}",
            "dir=in",
            "action=block",
            f"remoteip={ip}",
            "protocol=any",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"[FIREWALL] Rule added: block inbound from {ip}")
    else:
        print(f"[FIREWALL ERROR] Could not block {ip}: {result.stderr.strip()}")


def unblock_ip(ip):
    rule_name = f"{RULE_PREFIX}_{ip}"
    result = subprocess.run(
        [
            "netsh", "advfirewall", "firewall", "delete", "rule",
            f"name={rule_name}",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"[FIREWALL] Rule removed: unblocked {ip}")
    else:
        print(f"[FIREWALL ERROR] Could not unblock {ip}: {result.stderr.strip()}")


def cleanup_all_rules():
    subprocess.run(
        [
            "netsh", "advfirewall", "firewall", "delete", "rule",
            f"name={RULE_PREFIX}",
        ],
        capture_output=True,
    )
    print("[FIREWALL] All blocker rules cleaned up.")