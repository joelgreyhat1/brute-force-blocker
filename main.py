import argparse
from blocker.watcher import tail_log
from blocker.detector import BruteForceDetector
from blocker.firewall import block_ip, unblock_ip, cleanup_all_rules

def main():
    parser = argparse.ArgumentParser(description="Brute-force login blocker — watches a log file and blocks attacking IPs via Windows Firewall.")
    parser.add_argument("--log", default="auth.log", help="Log file to watch (default: auth.log)")
    parser.add_argument("--threshold", type=int, default=5, help="Failures before blocking (default: 5)")
    parser.add_argument("--window", type=int, default=60, help="Time window in seconds (default: 60)")
    parser.add_argument("--ban-duration", type=int, default=300, help="Ban duration in seconds (default: 300)")
    args = parser.parse_args()

    detector = BruteForceDetector(
        threshold=args.threshold,
        window=args.window,
        ban_duration=args.ban_duration,
    )

    print(f"Watching {args.log} for brute-force attempts...")
    print(f"  Threshold   : {args.threshold} failures in {args.window}s")
    print(f"  Ban duration: {args.ban_duration}s\n")

    try:
        for line in tail_log(args.log):
            ip = detector.parse_failure(line)
            if not ip:
                continue

            detector.record_failure(ip)

            if detector.should_block(ip) and ip not in detector.blocked_ips:
                detector.mark_blocked(ip)
                block_ip(ip)

    except KeyboardInterrupt:
        print("\nStopping blocker...")
        cleanup_all_rules()
        print("Done.")

if __name__ == "__main__":
    main()