import time
import os

def tail_log(filepath):
    # wait for the log file to exist if it doesn't yet
    while not os.path.exists(filepath):
        print(f"Waiting for {filepath} to be created...")
        time.sleep(2)

    with open(filepath, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if line:
                yield line.strip()
            else:
                time.sleep(0.5)