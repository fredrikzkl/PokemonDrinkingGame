"""
File watcher that rebuilds the board whenever source files change.
Usage: python watch.py [--tileRotation]
"""

import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_DIRS = [
    "assets",
    "src",
]

DEBOUNCE_SECONDS = 0.5


class RebuildHandler(FileSystemEventHandler):
    def __init__(self, extra_args):
        self.extra_args = extra_args
        self.last_trigger = 0

    def _should_watch(self, path):
        return any(
            path.endswith(ext)
            for ext in (".yaml", ".yml", ".py", ".txt", ".png", ".jpg", ".jpeg", ".webp")
        )

    def on_any_event(self, event):
        if event.is_directory:
            return
        if not self._should_watch(event.src_path):
            return

        now = time.time()
        if now - self.last_trigger < DEBOUNCE_SECONDS:
            return
        self.last_trigger = now

        print(f"\n--- Change detected: {event.src_path} ---")
        self._rebuild()

    def _rebuild(self):
        cmd = [sys.executable, "main.py"] + self.extra_args
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.stdout:
                print(result.stdout)
            if result.returncode != 0 and result.stderr:
                print(f"ERROR:\n{result.stderr}")
            elif result.returncode == 0:
                print("--- Rebuild complete ---")
        except subprocess.TimeoutExpired:
            print("ERROR: Build timed out after 60s")
        except Exception as e:
            print(f"ERROR: {e}")


def main():
    extra_args = sys.argv[1:]
    handler = RebuildHandler(extra_args)

    print("Watching for changes... (Ctrl+C to stop)")
    print(f"  Flags: {extra_args or '(none)'}")
    print(f"  Dirs: {WATCHED_DIRS}")

    handler._rebuild()

    observer = Observer()
    for path in WATCHED_DIRS:
        observer.schedule(handler, path, recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped watching.")
    observer.join()


if __name__ == "__main__":
    main()
