#!/usr/bin/env python
"""
Convert all AVIF and WebP images in media/products/ to PNG (for better PDF support).
Usage: python manage.py shell < convert_product_images.py
or:    python convert_product_images_standalone.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FashioHub.settings')
django.setup()

from django.conf import settings
from PIL import Image
import shutil

media_root = getattr(settings, 'MEDIA_ROOT', None) or os.path.join(settings.BASE_DIR, 'media')
products_dir = os.path.join(media_root, 'products')

if not os.path.exists(products_dir):
    print(f"Products directory not found: {products_dir}")
    exit(1)

avif_images = [f for f in os.listdir(products_dir) if f.lower().endswith('.avif')]
webp_images = [f for f in os.listdir(products_dir) if f.lower().endswith('.webp')]

unsupported = avif_images + webp_images

if not unsupported:
    print("✓ No AVIF or WebP images found. No conversion needed.")
    exit(0)

print(f"Found {len(unsupported)} unsupported images:")
for fname in unsupported:
    print(f"  - {fname}")

print("\nConverting to PNG...")
for fname in unsupported:
    src_path = os.path.join(products_dir, fname)
    dst_name = os.path.splitext(fname)[0] + '.png'
    dst_path = os.path.join(products_dir, dst_name)
    
    try:
        print(f"  Converting {fname} → {dst_name}...", end=' ')
        img = Image.open(src_path)
        img_rgb = img.convert('RGB')
        img_rgb.save(dst_path, 'PNG', quality=90)
        
        # Backup original
        backup_path = src_path + '.bak'
        shutil.move(src_path, backup_path)
        print(f"✓ (backup: {os.path.basename(backup_path)})")
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n✓ Conversion complete. Update product images in the database to point to .png files.")
