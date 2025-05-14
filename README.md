# 🎨 Image Compressor & Decompressor

> *Shrink & restore your images in a flash!* 🚀

## ✨ Key Features
- **`compress_with_palette()`** → fast, palette-based quantization  
- **`load_from_palette()`** → full RGBA reconstruction  
- **RGB/RGBA** support  
- Adjustable **tolerance** for size vs. quality  

## ⚙️ Usage
```bash
# 1) Compress → compressed_palette.npz
python compressor.py

# 2) Decompress → reconstructed.png
python compressor.py
