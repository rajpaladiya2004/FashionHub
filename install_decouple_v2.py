import subprocess
import sys
import os

print(f"Running install with {sys.executable}")
print(f"Sys Path: {sys.path}")

try:
    # Try installing with --user to avoid permission issues
    print("Attempting pip install --user python-decouple...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "python-decouple"])
    print("SUCCESS_INSTALL_USER")
except subprocess.CalledProcessError as e:
    print(f"FAILED_INSTALL_USER: {e}")
    # Fallback to normal install if --user fails (though unlikely to help if it failed before)
    try:
         print("Attempting pip install python-decouple (no --user)...")
         subprocess.check_call([sys.executable, "-m", "pip", "install", "python-decouple"])
         print("SUCCESS_INSTALL_GLOBAL")
    except subprocess.CalledProcessError as e2:
         print(f"FAILED_INSTALL_GLOBAL: {e2}")

# Verify import
try:
    import decouple
    print(f"VERIFY_IMPORT: Success, file: {decouple.__file__}")
except ImportError:
    print("VERIFY_IMPORT: Failed")
