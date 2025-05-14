"""
Copyright © 2025 Ahisek Rao. All rights reserved.
This code is protected by copyright law. Unauthorized copying or reproduction of this file,
via any medium, is strictly prohibited without the express permission of the author.

Author: Ahisek Rao
Description: This script allows you to compress images using color quantization into a palette format
             and later reconstruct them using the saved palette and index map.
"""

import numpy as np
from PIL import Image

def compress_with_palette(img_array: np.ndarray, tolerance: int = 10, output_file="compressed_palette.npz"):
    """
    Compress an RGBA image by quantizing its color values into discrete buckets and storing a color palette.

    Parameters:
        img_array (np.ndarray): Input image as an H×W×(3 or 4) NumPy array (RGB or RGBA).
        tolerance (int): The color quantization step size. Smaller values preserve more color detail.
        output_file (str): File path to save the compressed .npz file.

    Returns:
        tuple: The color palette (Px4 array) and the index map (HxW array).
    """
    # Ensure the input has 4 channels (RGBA)
    if img_array.ndim != 3 or img_array.shape[2] not in (3, 4):
        raise ValueError("Expected H×W×3 or H×W×4 array.")
    if img_array.shape[2] == 3:
        alpha = np.full(img_array.shape[:2] + (1,), 255, dtype=img_array.dtype)
        img_array = np.dstack((img_array, alpha))

    H, W, _ = img_array.shape

    # Reduce color precision by quantizing using the tolerance
    quant = (img_array // tolerance) * tolerance
    np.clip(quant, 0, 255, out=quant)

    # Flatten image to list of RGBA values and find unique ones
    flat = quant.reshape(-1, 4)
    palette, inverse = np.unique(flat, axis=0, return_inverse=True)

    # Choose the smallest possible datatype for indices
    max_idx = palette.shape[0] - 1
    if max_idx < 2**8:
        idx_dtype = np.uint8
    elif max_idx < 2**16:
        idx_dtype = np.uint16
    else:
        idx_dtype = np.uint32

    indices = inverse.astype(idx_dtype).reshape(H, W)

    # Save the palette and the index map to a compressed file
    np.savez_compressed(output_file, palette=palette, indices=indices)
    print(f"Saved palette ({palette.shape[0]} colors) + index map ({H}×{W}) → '{output_file}'")
    return palette, indices

def load_from_palette(file_path="compressed_palette.npz", save_image_path="reconstructed.png"):
    """
    Reconstruct an RGBA image using a saved palette and index map.

    Parameters:
        file_path (str): Path to the .npz file containing 'palette' and 'indices'.
        save_image_path (str): Where to save the reconstructed image.

    Returns:
        np.ndarray: The reconstructed RGBA image as an H×W×4 NumPy array.
    """
    with np.load(file_path) as data:
        palette = data["palette"]        # shape (P, 4)
        indices = data["indices"]        # shape (H, W)

    H, W = indices.shape

    # Use the palette and index map to reconstruct the image
    img = palette[indices]  # Fancy indexing
    img = img.astype(np.uint8)
    Image.fromarray(img, "RGBA").save(save_image_path)
    print(f"Reconstructed image saved → '{save_image_path}'")
    return img

if __name__ == "__main__":
    mode = input("1) Compress → palette.npz\n2) Load → image\nChoose 1 or 2: ")
    if mode == "1":
        path = input("Image path: ")
        out = input("Output .npz [compressed_palette.npz]: ") or "compressed_palette.npz"
        tol = int(input("Tolerance [10]: ") or 10)
        arr = np.array(Image.open(path).convert("RGBA"))
        compress_with_palette(arr, tolerance=tol, output_file=out)

    elif mode == "2":
        inp = input("Input .npz [compressed_palette.npz]: ") or "compressed_palette.npz"
        out = input("Output image [reconstructed.png]: ") or "reconstructed.png"
        load_from_palette(inp, save_image_path=out)

    else:
        print("Invalid choice.")
