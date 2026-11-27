import os
import glob
import time

base_dir = r'c:\Users\test\Videos\Office'
now = time.time()
two_hours_ago = now - 7200

print("Files modified in the last 2 hours:")
for root, dirs, files in os.walk(base_dir):
    for f in files:
        fp = os.path.join(root, f)
        try:
            mtime = os.path.getmtime(fp)
            if mtime > two_hours_ago:
                print(f"{time.ctime(mtime)} | {os.path.getsize(fp):>10} bytes | {fp}")
        except Exception as e:
            pass

print("\nChecking all files in data/IAOL:")
for root, dirs, files in os.walk(os.path.join(base_dir, 'data', 'IAOL')):
    for f in files:
        fp = os.path.join(root, f)
        print(f"{time.ctime(os.path.getmtime(fp))} | {os.path.getsize(fp):>10} bytes | {fp}")
