[English Version] | [Русская версия ниже](#README_RU.md)
# ComfyUI-Orakul-SVP

**Dual Export Node for ComfyUI — PNG to /output + 16-bit RAW TIFF to /output/temp_svp**

> A simple solution for saving generation results in two formats simultaneously:  
> standard PNG to ComfyUI `/output` and lossless 16-bit TIFF to `/output/temp_svp`.  
> Full batch support, accumulation mode, and sequential file numbering.

---

## Why You Need This

ComfyUI saves PNG in 8-bit by default. For stock photography, print, and professional post-processing this isn't enough — you lose half the tonal range the moment you hit Save.

**OrakulSVPNode** solves this in a single node:

- ✅ PNG saved normally via ComfyUI (`/output`) — for preview, web, stock upload
- ✅ 16-bit RAW TIFF saved to `/output/temp_svp` — next to PNG, in one place
- ✅ No TIFF compression (`COMPRESSION = NONE`) — zero data loss
- ✅ Full range `0–65535` from float tensor `0.0–1.0`
- ✅ Full batch support — every frame saved as a separate file
- ✅ Accumulation mode — existing files are never deleted, sequential numbering `ORAKUL_RAW_0001.tif`
- ✅ Trilingual console logs — UA / RU / EN

---

## File Structure

```
ComfyUI/
├── output/
│   ├── ComfyUI_00001_.png       ← standard PNG from Save Image node
│   └── temp_svp/
│       ├── ORAKUL_RAW_0001.tif  ← 16-bit RAW TIFF
│       ├── ORAKUL_RAW_0002.tif
│       └── ...
└── custom_nodes/
    └── ComfyUI-Orakul-SVP/
        ├── orakul_svp_node.py
        ├── __init__.py
        └── README.md
```

---

## Installation

**1. Clone into custom_nodes folder:**

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/YOUR_USERNAME/ComfyUI-Orakul-SVP
```

**2. Make sure OpenCV is installed:**

```bash
pip install opencv-python-headless
```

**3. Restart ComfyUI.**

The node will appear in the **`Orakul Studio`** category.

---

## Usage

1. Add the **OrakulSVPNode** to your workflow
2. Connect `IMAGE` output from `KSampler` (or any image source)
3. Connect the node's output to the standard **`Save Image`** node
4. Run generation

```
KSampler → OrakulSVPNode → Save Image
```

**Result:**
- PNG → `ComfyUI/output/` (via Save Image as usual)
- TIFF 16-bit → `ComfyUI/output/temp_svp/ORAKUL_RAW_0001.tif`, `_0002.tif`, ...

---

## Accumulation Mode

The node works in **accumulation mode** — files are never overwritten or deleted.

On each new run the node finds the highest existing index and continues numbering from there:

```
Run 1 (batch=1): ORAKUL_RAW_0001.tif
Run 2 (batch=4): ORAKUL_RAW_0002.tif, _0003.tif, _0004.tif, _0005.tif
Run 3 (batch=1): ORAKUL_RAW_0006.tif
```

To reset numbering — simply clear the `output/temp_svp/` folder manually.

---

## Technical Details

| Parameter | Value |
|---|---|
| TIFF format | 16-bit unsigned integer (uint16) |
| Compression | NONE (IMWRITE_TIFF_COMPRESSION = 1) |
| Color space | RGB → BGR (OpenCV) |
| Range | 0.0–1.0 float → 0–65535 uint16 |
| Numbering | `ORAKUL_RAW_0001.tif` (4 digits, sequential) |
| File size | ~24–25 MB at 2752×1536 |
| Batch | Full support, each frame as individual file |

---

## File Size Comparison

| Format | Resolution | Size |
|---|---|---|
| PNG 8-bit | 2752×1536 | ~4–6 MB |
| TIFF 16-bit RAW | 2752×1536 | ~24–25 MB |

---

## Console Output Example

```
🛠️⚙️Orakul Engine: MASTER RAW (TIFF 16-BIT) mode is active. Accumulation mode.
🎞️🛠️Orakul Engine: Adding a Batch (4 frames) to existing ones...
 -> 👍Added: ORAKUL_RAW_0003.tif
 -> 👍Added: ORAKUL_RAW_0004.tif
 -> 👍Added: ORAKUL_RAW_0005.tif
 -> 👍Added: ORAKUL_RAW_0006.tif
```

---

## Compatibility

- ComfyUI (all current versions)
- Python 3.10+
- PyTorch (CUDA / CPU)
- OpenCV `opencv-python` or `opencv-python-headless`
- Windows / Linux

---

## Who Is This For

- **Stock photographers** — upload to Adobe Stock, Shutterstock, Getty at full quality
- **Print & prepress** — TIFF 16-bit accepted directly without conversion
- **Post-processing** — open in Photoshop / Lightroom with full tonal range intact
- **Archiving** — store master files with zero quality degradation

---

## Roadmap

- [ ] Custom save folder via node parameter
- [ ] LZW/ZIP compression option to save disk space
- [ ] EXIF/IPTC metadata in TIFF (for stock workflows)
- [ ] EXR 32-bit support for HDR pipelines

---

## Author

**Orakul Studio** — Chernihiv, Ukraine 🇺🇦  
Flux2 · ComfyUI · RTX 4090 · No quantization · No compromises

---

## License

MIT License — use it, fork it, improve it.
