#!/usr/bin/env python
"""Test AVIF to JPEG conversion"""
from PIL import Image as PILImage
from io import BytesIO
import os

avif_path = r'd:\web\FashioHub\media\products\1.avif'

print(f"Testing AVIF conversion...")
print(f"File: {avif_path}")
print(f"Exists: {os.path.exists(avif_path)}")

try:
    # Try to open AVIF
    print("\nAttempting to open AVIF with PIL...")
    pil_img = PILImage.open(avif_path)
    print(f"✗ PIL opened AVIF (unexpected - AVIF not supported)")
    print(f"  Image mode: {pil_img.mode}")
    print(f"  Image size: {pil_img.size}")
except Exception as e:
    print(f"✗ PIL failed to open AVIF: {type(e).__name__}: {e}")
    print(f"\nPillow AVIF support is NOT available on this system")
    print(f"AVIF images will show as '-' in the invoice")
    
    # Check Pillow version and plugins
    print(f"\nPillow Info:")
    print(f"  Version: {PILImage.PILLOW_VERSION if hasattr(PILImage, 'PILLOW_VERSION') else 'unknown'}")
    print(f"  Available formats: {PILImage.OPEN.keys() if hasattr(PILImage, 'OPEN') else 'unknown'}")
