import time
from collections import defaultdict

class BruteForceDetector:
    def __init__(self, threshold=5, window=60, ban_duration=300):
        self.threshold = threshold      
        self.window = window            
        self.ban_duration = ban_duration 
        self.failure_times = defaultdict(list)
        self.blocked_ips = {}

    def parse_failure(self, line):
       
        if "FAILED_LOGIN" not in line:
            return None
        try:
            parts = {k: v for k, v in (p.split("=") for p in line.split() if "=" in p)}
            return parts.get("ip")
        except Exception:
            return None

    def record_failure(self, ip):
        now = time.time()
        self.failure_times[ip].append(now)
        
        self.failure_times[ip] = [t for t in self.failure_times[ip] if now - t < self.window]

    def should_block(self, ip):
        if ip in self.blocked_ips:
           
            if time.time() - self.blocked_ips[ip] > self.ban_duration:
                del self.blocked_ips[ip]
                print(f"[UNBLOCKED] {ip} — ban expired after {self.ban_duration}s")
                return False
            return True
        return len(self.failure_times.get(ip, [])) >= self.threshold

    def mark_blocked(self, ip):
        self.blocked_ips[ip] = time.time()
        count = len(self.failure_times.get(ip, []))
        print(f"[BLOCKED] {ip} — {count} failures in {self.window}s")