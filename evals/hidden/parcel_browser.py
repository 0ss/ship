"""Exercise the parcel journey in headless Chrome without repository dependencies."""
import http.server
import json
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path

CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
SCRIPT = Path(__file__).with_name("parcel_click.mjs")


def check(workdir):
    if not CHROME.exists():
        return {"error": "Chrome is unavailable on this host"}
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(workdir / "web"), **kwargs)

        def log_message(self, *_args):
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    profile = Path(tempfile.mkdtemp(prefix="ship-parcel-chrome-"))
    chrome = subprocess.Popen([
        str(CHROME), "--headless", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
        "--remote-debugging-port=0", "--remote-allow-origins=*", f"--user-data-dir={profile}",
        "about:blank",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        port_file = profile / "DevToolsActivePort"
        for _ in range(100):
            if port_file.exists():
                break
            if chrome.poll() is not None:
                return {"error": f"Chrome exited {chrome.returncode}"}
            time.sleep(0.05)
        if not port_file.exists():
            return {"error": "Chrome debugging port never appeared"}
        debug_port = port_file.read_text().splitlines()[0]
        page_url = f"http://127.0.0.1:{server.server_port}/map.html"
        run = subprocess.run(["node", str(SCRIPT), debug_port, page_url],
                             capture_output=True, text=True, timeout=20)
        if run.returncode:
            return {"error": run.stderr[-500:]}
        return json.loads(run.stdout)
    finally:
        chrome.terminate()
        try:
            chrome.wait(timeout=5)
        except subprocess.TimeoutExpired:
            chrome.kill()
        server.shutdown()
        server.server_close()
        shutil.rmtree(profile, ignore_errors=True)


if __name__ == "__main__":
    import sys
    print(json.dumps(check(Path(sys.argv[1]).resolve())))
