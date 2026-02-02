#!/usr/bin/env python
"""Test AVIF support with pillow-heif"""
import os

print("Testing AVIF support with pillow-heif...")
print("=" * 70)

try:
    import pillow_heif
    print("✓ pillow_heif imported successfully")
    
    # Register HEIF/AVIF opener
    pillow_heif.register_heif_opener()
    print("✓ HEIF/AVIF opener registered")
    
    from PIL import Image as PILImage
    
    avif_path = r'd:\web\FashioHub\media\products\1.avif'
    print(f"\nOpening AVIF: {avif_path}")
    
    try:
        img = PILImage.open(avif_path)
        print(f"✓ AVIF opened successfully!")
        print(f"  Size: {img.size}")
        print(f"  Mode: {img.mode}")
        
        # Test conversion
        print(f"\nConverting to JPEG...")
        rgb_img = img.convert('RGB')
        from io import BytesIO
        buffer = BytesIO()
        rgb_img.save(buffer, format='JPEG', quality=85)
        print(f"✓ Conversion successful ({len(buffer.getvalue())} bytes)")
        
    except Exception as e:
        print(f"✗ Failed to open AVIF: {e}")
        
except ImportError as e:
    print(f"✗ pillow_heif import failed: {e}")
