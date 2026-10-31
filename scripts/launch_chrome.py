import subprocess
import os
import sys

# Prefer user-space Chromium or Chrome without breakaway flags
chrome_paths = [
    r"C:\Users\amank\AppData\Local\ms-playwright\chromium-1248\chrome-win64\chrome.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]

target_exe = None
for p in chrome_paths:
    if os.path.exists(p):
        target_exe = p
        break

if not target_exe:
    print("Could not find Chrome executable!")
    sys.exit(1)

profile_dir = os.path.expandvars(r"%LOCALAPPDATA%\Temp\civicflow_browser_profile")
os.makedirs(profile_dir, exist_ok=True)

urls = [
    "http://localhost:3000",
    "http://localhost:3000/applications/app-mvwn5q0p-o0pgpf/workspace",
]

cmd = [
    target_exe,
    f"--user-data-dir={profile_dir}",
    "--no-first-run",
    "--no-default-browser-check",
    "--start-maximized",
] + urls

print(f"Launching {target_exe}...")
p = subprocess.Popen(cmd)
print(f"Chrome launched with PID {p.pid}!")
