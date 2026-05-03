[English Version] | [Русская версия ниже](#русская-версия)
# ComfyUI-Orakul-SVP

**Professional Dual/Triple Export Node — PNG + TIFF 16-bit + EXR 32-bit float**

> One node. Three formats. Zero compression. Zero compromise.  
> Designed for Flux2 native resolution workflows on high-end hardware.


---

## What It Does

ComfyUI saves PNG in 8-bit by default. That's fine for web. It's not fine for print, stock, or HDR post-processing — you lose half the tonal range the moment you click Save.

**OrakulSVPNode** plugs directly into your workflow after KSampler and silently exports master files in parallel:

| Format | Bit depth | Use case |
|---|---|---|
| PNG | 8-bit | Web, preview, stock upload (via Save Image) |
| TIFF | 16-bit RAW | Print, Photoshop, Lightroom, Adobe Stock masters |
| EXR | 32-bit float | HDR compositing, VFX, Nuke, DaVinci Resolve |

All three simultaneously if you want. Or any combination. Your call.

---

## Features

- ✅ **TIFF 16-bit** — `uint16`, zero compression (`IMWRITE_TIFF_COMPRESSION = 1`), full `0–65535` range
- ✅ **EXR 32-bit float** — true HDR, `float32`, full linear light data preserved
- ✅ **Full batch support** — every frame in the batch saved as individual file
- ✅ **Accumulation mode** — existing files never deleted, sequential numbering continues
- ✅ **Toggle per format** — enable/disable TIFF and EXR independently via node UI
- ✅ **Safe EXR writing** — uses isolated subprocess to set `OPENCV_IO_ENABLE_OPENEXR=1` before cv2 loads, bypassing ComfyUI's already-initialized environment
- ✅ **Auto cleanup** — temp files from EXR subprocess removed after each frame
- ✅ **Trilingual console logs** — RU / UA / EN

---

## File Structure

```
ComfyUI/
├── output/
│   ├── ComfyUI_00001_.png          ← 8-bit PNG via Save Image node
│   └── temp_svp/
│       ├── ORAKUL_RAW_0001.tif     ← 16-bit RAW TIFF
│       ├── ORAKUL_RAW_0001.exr     ← 32-bit float EXR
│       ├── ORAKUL_RAW_0002.tif
│       ├── ORAKUL_RAW_0002.exr
│       └── ...
└── custom_nodes/
    └── ComfyUI-Orakul-SVP/
        ├── orakul_svp_node.py
        ├── __init__.py
        └── README.md
```

---

## Installation

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/OrakulStudio/ComfyUI-Orakul-SVP
pip install opencv-python-headless
```

Restart ComfyUI. Node appears in **`Orakul Studio`** category.

---

## Usage

```
KSampler → OrakulSVPNode → Save Image
```

1. Add **OrakulSVPNode** to your workflow
2. Connect `IMAGE` from KSampler (or any image source)
3. Connect output to standard **Save Image** node
4. Toggle `save_tiff` and `save_exr` as needed in the node UI
5. Run

**Node inputs:**

| Input | Type | Default | Description |
|---|---|---|---|
| `images` | IMAGE | — | Image tensor from pipeline |
| `save_tiff` | BOOLEAN | `True` | Save 16-bit TIFF to temp_svp |
| `save_exr` | BOOLEAN | `False` | Save 32-bit EXR to temp_svp |

---

## Accumulation Mode

The node never deletes existing files. Each run continues numbering from where the last run stopped:

```
Run 1 (batch=2, TIFF+EXR): ORAKUL_RAW_0001.tif, ORAKUL_RAW_0001.exr
                             ORAKUL_RAW_0002.tif, ORAKUL_RAW_0002.exr
Run 2 (batch=1, TIFF only): ORAKUL_RAW_0003.tif
Run 3 (batch=1, EXR only):  ORAKUL_RAW_0004.exr
```

To reset — manually clear `output/temp_svp/`.

---

## Why Subprocess for EXR?

OpenCV requires `OPENCV_IO_ENABLE_OPENEXR=1` to be set **before** the library is imported. ComfyUI imports cv2 at startup — long before your node runs. Setting the env variable at runtime has no effect.

The solution: write a tiny isolated Python script and execute it via `subprocess.run()` using ComfyUI's own interpreter (`sys.executable`). The subprocess starts fresh, sets the variable first, then writes the EXR. Temp script and temp `.npy` data file are removed immediately after.

No external dependencies. No monkey-patching. No hacks that break other nodes.

---

## Technical Details

| Parameter | TIFF | EXR |
|---|---|---|
| Bit depth | 16-bit uint | 32-bit float |
| Compression | NONE | OpenEXR default |
| Color space | RGB→BGR (OpenCV) | RGB→BGR (OpenCV) |
| Value range | 0–65535 | 0.0–1.0 float |
| File size @ 2752×1536 | ~24–25 MB | ~48–50 MB |

---

## Console Output Example

```
RU 🛠️⚙️Orakul Engine: Режим MASTER RAW инициализирован TIFF(16-bit) EXR(32-bit float).
RU 🎞️🛠️Orakul Engine: Добавление батча (2 кадров)...
 ->EN 👍 TIFF 16-bit saved: ORAKUL_RAW_0001.tif
 ->EN 👍 EXR 32-bit float saved: ORAKUL_RAW_0001.exr
 ->EN 👍 TIFF 16-bit saved: ORAKUL_RAW_0002.tif
 ->EN 👍 EXR 32-bit float saved: ORAKUL_RAW_0002.exr
```

---

## Compatibility

- ComfyUI (all current versions)
- Python 3.10+
- PyTorch (CUDA / CPU)
- `opencv-python` or `opencv-python-headless`
- Windows / Linux

---

## Who Is This For

- **Stock photographers** — upload TIFF masters to Adobe Stock, Shutterstock, Getty
- **Print & prepress** — 16-bit TIFF accepted directly, no conversion needed
- **VFX / compositing** — EXR 32-bit for Nuke, DaVinci Resolve, Blender compositor
- **Archiving** — store master files with full data intact, re-export to any format later

---

## Roadmap

- [ ] Custom output folder via node parameter
- [ ] LZW/ZIP compression option for TIFF
- [ ] EXIF/IPTC metadata embedding (for stock workflows)
- [ ] Multi-layer EXR with separate R/G/B/A channels

---

## Author

**Orakul Studio** — Chernihiv, Ukraine 🇺🇦  
Flux2 · ComfyUI · RTX 4090 · No quantization · No compromises

---

## License

MIT — use it, fork it, improve it.


# Русская версия  
[Back to English / Наверх](#comfyui-orakul-svp)

# ComfyUI-Orakul-SVP

**Dual Export Node for ComfyUI — PNG to /output + 16-bit RAW TIFF to /output/temp_svp**

> Простое решение для сохранения результатов генерации в двух форматах одновременно:  
> стандартный PNG в папку ComfyUI `/output` и архивный 16-bit TIFF без сжатия в `/output/temp_svp`.  
> Поддерживает batch, накопительный режим и сквозную нумерацию файлов.

---

## Зачем это нужно

ComfyUI по умолчанию сохраняет PNG в 8 бит. Для стоковой фотографии, печати и профессиональной постобработки этого недостаточно — теряется половина тонального диапазона.

**OrakulSVPNode** решает это в одну ноду:

- ✅ PNG сохраняется стандартно через ComfyUI (`/output`) — для превью, веба, стока
- ✅ 16-bit RAW TIFF сохраняется в `/output/temp_svp` — рядом с PNG, в одном месте
- ✅ Нет сжатия TIFF (`COMPRESSION = NONE`) — нулевых потерь данных
- ✅ Полный диапазон `0–65535` из float тензора `0.0–1.0`
- ✅ Полная поддержка batch — каждый кадр сохраняется отдельным файлом
- ✅ Накопительный режим — старые файлы не удаляются, сквозная нумерация `ORAKUL_RAW_0001.tif`
- ✅ Трёхязычные логи в консоли — UA / RU / EN

---

## Структура файлов

```
ComfyUI/
├── output/
│   ├── ComfyUI_00001_.png       ← стандартный PNG от Save Image
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

## Установка

**1. Клонировать в папку custom_nodes:**

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/YOUR_USERNAME/ComfyUI-Orakul-SVP
```

**2. Убедиться что установлен OpenCV:**

```bash
pip install opencv-python-headless
```

**3. Перезапустить ComfyUI.**

Нода появится в категории **`Orakul Studio`**.

---

## Использование

1. Добавить ноду **OrakulSVPNode** в workflow
2. Подключить выход `IMAGE` от `KSampler` (или любого другого источника)
3. Подключить выход ноды к стандартному **`Save Image`** узлу ComfyUI
4. Запустить генерацию

```
KSampler → OrakulSVPNode → Save Image
```

**Результат:**
- PNG → `ComfyUI/output/` (через Save Image как обычно)
- TIFF 16-bit → `ComfyUI/output/temp_svp/ORAKUL_RAW_0001.tif`, `_0002.tif`, ...

---

## Накопительный режим

Нода работает в режиме **накопления** — файлы не перезаписываются и не удаляются.

При каждом новом прогоне нода находит максимальный существующий индекс и продолжает нумерацию:

```
Прогон 1 (batch=1): ORAKUL_RAW_0001.tif
Прогон 2 (batch=4): ORAKUL_RAW_0002.tif, _0003.tif, _0004.tif, _0005.tif
Прогон 3 (batch=1): ORAKUL_RAW_0006.tif
```

Чтобы начать нумерацию заново — просто вручную очистите папку `output/temp_svp/`.

---

## Технические детали

| Параметр | Значение |
|---|---|
| Формат TIFF | 16-bit unsigned integer (uint16) |
| Сжатие | NONE (IMWRITE_TIFF_COMPRESSION = 1) |
| Цветовое пространство | RGB → BGR (OpenCV) |
| Диапазон | 0.0–1.0 float → 0–65535 uint16 |
| Нумерация | `ORAKUL_RAW_0001.tif` (4 знака, сквозная) |
| Размер файла | ~24–25 MB при 2752×1536 |
| Batch | Полная поддержка, каждый кадр отдельный файл |

---

## Пример веса файлов

| Формат | Разрешение | Размер |
|---|---|---|
| PNG 8-bit | 2752×1536 | ~4–6 MB |
| TIFF 16-bit RAW | 2752×1536 | ~24–25 MB |

---

## Пример вывода в консоли

```
🛠️⚙️Orakul Engine: MASTER RAW (TIFF 16-BIT) mode is active. Accumulation mode.
🎞️🛠️Orakul Engine: Adding a Batch (4 frames) to existing ones...
 -> 👍Added: ORAKUL_RAW_0003.tif
 -> 👍Added: ORAKUL_RAW_0004.tif
 -> 👍Added: ORAKUL_RAW_0005.tif
 -> 👍Added: ORAKUL_RAW_0006.tif
```

---

## Совместимость

- ComfyUI (все актуальные версии)
- Python 3.10+
- PyTorch (CUDA / CPU)
- OpenCV `opencv-python` или `opencv-python-headless`
- Windows / Linux

---

## Для кого это

- **Стоковые фотографы** — загружаете на Adobe Stock, Shutterstock, Getty с максимальным качеством
- **Полиграфия** — TIFF 16-bit принимается напрямую в препресс без конвертации
- **Постобработка** — открываете в Photoshop / Lightroom с полным тональным диапазоном
- **Архивирование** — храните мастер-файлы без деградации качества

---

## Roadmap

- [ ] Выбор папки сохранения через параметр ноды
- [ ] Опция сжатия LZW/ZIP для экономии места
- [ ] Метаданные EXIF/IPTC в TIFF (для стока)
- [ ] Поддержка EXR 32-bit для HDR workflow

---

## Автор

**Orakul Studio** — Chernihiv, Ukraine 🇺🇦  
Flux2 · ComfyUI · RTX 4090 · No quantization · No compromises

---

## Лицензия

MIT License — используй, форкай, улучшай.

[Back to English / Наверх](#comfyui-orakul-svp)


