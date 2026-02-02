#!/usr/bin/env python
import os
import sys
from PIL import Image as PILImage
from io import BytesIO

img_path = r"D:\web\FashioHub\media\products\1.avif"

try:
    print(f"Opening image: {img_path}")
    pil_img = PILImage.open(img_path)
    print(f"  ✓ Opened successfully")
    print(f"  Format: {pil_img.format}")
    print(f"  Size: {pil_img.size}")
    print(f"  Mode: {pil_img.mode}")
    
    print(f"Converting to RGB...")
    pil_img = pil_img.convert('RGB')
    print(f"  ✓ Converted to RGB")
    
    print(f"Saving to PNG buffer...")
    tmp_buf = BytesIO()
    pil_img.save(tmp_buf, format='PNG')
    tmp_buf.seek(0)
    print(f"  ✓ Saved to buffer")
    print(f"  Buffer size: {len(tmp_buf.getvalue())} bytes")
    
    print("\n✓ AVIF → PNG conversion successful!")
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
