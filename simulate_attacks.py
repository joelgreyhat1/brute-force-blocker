import time
import random
from datetime import datetime

LOG_FILE = "auth.log"

# simulates a brute-force attack from two different IPs
ATTACKING_IPS = ["192.168.1.50", "192.168.1.75"]
NORMAL_IP = "192.168.1.10"

def write_failure(ip, username="admin"):
    line = f"{datetime.utcnow().isoformat()} FAILED_LOGIN ip={ip} username={username}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
    print(f"[SIMULATED] Failed login from {ip}")

def simulate(burst_count=10, delay=0.3):
    print(f"Simulating attacks... writing to {LOG_FILE}")
    print(f"Normal traffic from {NORMAL_IP} (1 failure, shouldn't trigger block)")
    write_failure(NORMAL_IP)
    time.sleep(1)

    for attacker_ip in ATTACKING_IPS:
        print(f"\nBurst attack from {attacker_ip} ({burst_count} failures)...")
        for _ in range(burst_count):
            write_failure(attacker_ip)
            time.sleep(delay)

if __name__ == "__main__":
    simulate()