#!/usr/bin/env python
"""
Convert AVIF images to PNG format
This is needed because the system's Pillow doesn't support AVIF
"""
import os
import subprocess
import sys

avif_files = [
    r'd:\web\FashioHub\media\products\1.avif',
    r'd:\web\FashioHub\media\products\2.1.avif',
]

print("Checking for image conversion tools...")
print("=" * 70)

# Check for ImageMagick convert tool
try:
    result = subprocess.run(['magick', '--version'], capture_output=True, text=True)
    print(f"✓ ImageMagick found: {result.stdout.split(chr(10))[0]}")
    has_imagemagick = True
except:
    print(f"✗ ImageMagick not found")
    has_imagemagick = False

# Check for ffmpeg
try:
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
    print(f"✓ ffmpeg found")
    has_ffmpeg = True
except:
    print(f"✗ ffmpeg not found")
    has_ffmpeg = False

print("\n" + "=" * 70)

if not has_imagemagick and not has_ffmpeg:
    print("\n⚠️  No image conversion tools found!")
    print("\nTo fix AVIF image support, you need to install one of:")
    print("\n1. ImageMagick:")
    print("   Download from: https://imagemagick.org/script/download.php")
    print("   Or: choco install imagemagick")
    print("\n2. FFmpeg:")
    print("   Download from: https://ffmpeg.org/download.html")
    print("   Or: choco install ffmpeg")
    print("\n3. Alternative: Convert AVIF files manually using an online tool")
    print("   Go to: https://convertio.co/avif-png/")
    sys.exit(1)

print("\nConverting AVIF files to PNG...")
print("=" * 70)

for avif_file in avif_files:
    if not os.path.exists(avif_file):
        print(f"\n✗ File not found: {avif_file}")
        continue
    
    png_file = avif_file.replace('.avif', '.png')
    print(f"\nConverting: {os.path.basename(avif_file)}")
    print(f"  From: {avif_file}")
    print(f"  To:   {png_file}")
    
    try:
        if has_imagemagick:
            # Try ImageMagick
            subprocess.run(['magick', avif_file, png_file], check=True, capture_output=True)
            print(f"  ✓ Converted with ImageMagick")
        elif has_ffmpeg:
            # Try ffmpeg
            subprocess.run(['ffmpeg', '-i', avif_file, png_file], check=True, capture_output=True)
            print(f"  ✓ Converted with FFmpeg")
    except Exception as e:
        print(f"  ✗ Conversion failed: {e}")
        continue
    
    # Update database to point to PNG instead of AVIF
    if os.path.exists(png_file):
        print(f"  ✓ PNG file created successfully")

print("\n" + "=" * 70)
print("Next: Update database to use PNG files instead of AVIF")
