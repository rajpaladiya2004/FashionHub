import subprocess
import sys

print(f"Running install with {sys.executable}")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-decouple"])
    print("SUCCESS_INSTALL")
except subprocess.CalledProcessError as e:
    print(f"FAILED_INSTALL: {e}")
