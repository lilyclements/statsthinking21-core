#!/bin/bash
# Pre-build script for PreTeXt
# Copies images from images/ directory to external/ directory for PreTeXt build

echo "Copying images from images/ to external/ for PreTeXt build..."

# Create external directory if it doesn't exist
mkdir -p external

# Count and copy images
png_count=$(find images/ -maxdepth 1 -name "*.png" -type f 2>/dev/null | wc -l)
jpg_count=$(find images/ -maxdepth 1 -name "*.jpg" -type f 2>/dev/null | wc -l)
jpeg_count=$(find images/ -maxdepth 1 -name "*.jpeg" -type f 2>/dev/null | wc -l)

cp images/*.png external/ 2>/dev/null || true
cp images/*.jpg external/ 2>/dev/null || true
cp images/*.jpeg external/ 2>/dev/null || true

echo "Copied $png_count PNG files, $jpg_count JPG files, and $jpeg_count JPEG files."
echo "Images copied successfully."
echo "You can now run: pretext build html"
