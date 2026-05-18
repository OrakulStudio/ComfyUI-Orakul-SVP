[English Version] | [Русская версия ниже](#русская-версия)
# ComfyUI-Orakul-SVP

**Professional Dual/Triple Export Node  PNG + TIFF 16-bit + EXR 32-bit float**

> One node. Three formats. Zero compression. Zero compromise.  
> Designed for Flux2 native resolution workflows on high-end hardware.


---

## What It Does

ComfyUI saves PNG in 8-bit by default. That's fine for web. It's not fine for print, stock, or HDR post-processing  you lose half the tonal range the moment you click Save.

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

### Standard ComfyUI
Open your terminal and run the following commands:
```bash
cd ComfyUI/custom_nodes
git clone [https://github.com/OrakulStudio/ComfyUI-Orakul-SVP](https://github.com/OrakulStudio/ComfyUI-Orakul-SVP)
pip install opencv-python-headless

Restart ComfyUI. Node appears in **`Orakul Studio`** category.

---

## Usage

For Stability Matrix Users (Important Fix)
If you encounter the ModuleNotFoundError: No module named 'cv2' error, the standard terminal command will not work. You must install the dependency through the Matrix GUI:

Open Stability Matrix and navigate to the Packages tab.

Click the gear icon (Settings) on your ComfyUI package card.

Select Python Packages.

Type opencv-python-headless into the install field and click Install.

Restart ComfyUI.

Once installed, the nodes will appear in the Orakul Studio category.

```
KSampler → OrakulSVPNode → Save Image
```
## Simple and clean interface
<img width="967" height="531" alt="Снимок экрана 2026-05-03 092559" src="https://github.com/user-attachments/assets/a29702bb-a593-472e-826f-d1b05bfa6c3b" />


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
## Professional trilingual logging system (RU/UA/EN)
<img width="3133" height="1726" alt="Снимок экрана 2026-05-03 103633" src="https://github.com/user-attachments/assets/3b23e6fb-ba85-4cee-ba12-ca3c00b3c132" />


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

**Профессиональный экспорт из ComfyUI — PNG + TIFF 16-bit + EXR 32-bit float**

> Одна нода. Три формата. Без сжатия. Без компромиссов.  
> Создано для Flux2 в нативном разрешении на серьёзном железе.

🇬🇧 [English version](README_EN.md)

---

## Что это делает

ComfyUI по умолчанию сохраняет PNG в 8 бит. Для веба  нормально. Для печати, стока или HDR постобработки  нет: теряется половина тонального диапазона сразу при сохранении.

**OrakulSVPNode** встаёт в пайплайн после KSampler и молча экспортирует мастер-файлы параллельно:

| Формат | Битность | Применение |
|---|---|---|
| PNG | 8-bit | Веб, превью, загрузка на сток (через Save Image) |
| TIFF | 16-bit RAW | Печать, Photoshop, Lightroom, мастера для Adobe Stock |
| EXR | 32-bit float | HDR-композитинг, VFX, Nuke, DaVinci Resolve |

Все три одновременно  если нужно. Или любая комбинация. Переключается в UI ноды.

---

## Возможности

- ✅ **TIFF 16-bit** — `uint16`, нулевое сжатие (`IMWRITE_TIFF_COMPRESSION = 1`), полный диапазон `0–65535`
- ✅ **EXR 32-bit float** — настоящий HDR, `float32`, линейные данные света сохранены полностью
- ✅ **Полная поддержка batch** — каждый кадр батча сохраняется отдельным файлом
- ✅ **Накопительный режим** — существующие файлы не удаляются, нумерация продолжается
- ✅ **Раздельное управление** — TIFF и EXR включаются независимо в UI ноды
- ✅ **Безопасная запись EXR** — изолированный subprocess устанавливает `OPENCV_IO_ENABLE_OPENEXR=1` до загрузки cv2, обходя уже инициализированную среду ComfyUI
- ✅ **Автозачистка** — временные файлы EXR subprocess удаляются после каждого кадра
- ✅ **Трёхязычные логи** — RU / UA / EN

---

## Структура файлов

```
ComfyUI/
├── output/
│   ├── ComfyUI_00001_.png          ← 8-bit PNG через Save Image ноду
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

## Установка

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/OrakulStudio/ComfyUI-Orakul-SVP
pip install opencv-python-headless
```

Перезапустить ComfyUI. Нода появится в категории **`Orakul Studio`**.

---

## Использование

```
KSampler → OrakulSVPNode → Save Image
```
## Простой и чистый интерфейс
<img width="967" height="531" alt="Снимок экрана 2026-05-03 092559" src="https://github.com/user-attachments/assets/0fdf5c6f-ba58-4f40-a24e-3654e690dc85" />



1. Добавить **OrakulSVPNode** в workflow
2. Подключить `IMAGE` от KSampler (или любого источника)
3. Выход ноды подключить к стандартному **Save Image**
4. Включить `save_tiff` и/или `save_exr` в UI ноды
5. Запустить генерацию

**Входы ноды:**

| Вход | Тип | По умолчанию | Описание |
|---|---|---|---|
| `images` | IMAGE | — | Тензор изображения из пайплайна |
| `save_tiff` | BOOLEAN | `True` | Сохранить 16-bit TIFF в temp_svp |
| `save_exr` | BOOLEAN | `False` | Сохранить 32-bit EXR в temp_svp |

---

## Накопительный режим

Нода никогда не удаляет существующие файлы. Каждый прогон продолжает нумерацию с места остановки:

```
Прогон 1 (batch=2, TIFF+EXR): ORAKUL_RAW_0001.tif, ORAKUL_RAW_0001.exr
                                ORAKUL_RAW_0002.tif, ORAKUL_RAW_0002.exr
Прогон 2 (batch=1, только TIFF): ORAKUL_RAW_0003.tif
Прогон 3 (batch=1, только EXR):  ORAKUL_RAW_0004.exr
```

Для сброса — вручную очистить папку `output/temp_svp/`.

---

## Почему subprocess для EXR?

OpenCV требует установки `OPENCV_IO_ENABLE_OPENEXR=1` **до** импорта библиотеки. ComfyUI импортирует cv2 при запуске  задолго до вызова вашей ноды. Установка переменной в runtime не имеет эффекта.

Решение: записать крохотный изолированный Python-скрипт и выполнить его через `subprocess.run()` с интерпретатором ComfyUI (`sys.executable`). Subprocess стартует чистым, устанавливает переменную первым делом, записывает EXR. Временный скрипт и временный `.npy` файл удаляются сразу после.

Никаких внешних зависимостей. Никакого monkey-patching. Никаких хаков ломающих другие ноды.

---

## Технические детали

| Параметр | TIFF | EXR |
|---|---|---|
| Битность | 16-bit uint | 32-bit float |
| Сжатие | NONE | OpenEXR default |
| Цветовое пространство | RGB→BGR (OpenCV) | RGB→BGR (OpenCV) |
| Диапазон значений | 0–65535 | 0.0–1.0 float |
| Размер файла @ 2752×1536 | ~24–25 MB | ~48–50 MB |

---

## Пример вывода в консоли

```
RU 🛠️⚙️Orakul Engine: Режим MASTER RAW инициализирован TIFF(16-bit) EXR(32-bit float).
RU 🎞️🛠️Orakul Engine: Добавление батча (2 кадров)...
 ->RU 👍 TIFF 16-bit сохранен: ORAKUL_RAW_0001.tif
 ->RU 👍 EXR 32-bit float сохранен: ORAKUL_RAW_0001.exr
 ->RU 👍 TIFF 16-bit сохранен: ORAKUL_RAW_0002.tif
 ->RU 👍 EXR 32-bit float сохранен: ORAKUL_RAW_0002.exr
```

## Профессиональная трехъязычная система логирования (RU/UA/EN)
<img width="3133" height="1726" alt="Снимок экрана 2026-05-03 103633" src="https://github.com/user-attachments/assets/a273382a-bf77-4868-9e57-e5e875c7f9cd" />


---

## Совместимость

- ComfyUI (все актуальные версии)
- Python 3.10+
- PyTorch (CUDA / CPU)
- `opencv-python` или `opencv-python-headless`
- Windows / Linux

---

## Для кого это

- **Стоковые фотографы** — загружаете TIFF мастера на Adobe Stock, Shutterstock, Getty
- **Полиграфия** — TIFF 16-bit принимается напрямую в препресс без конвертации
- **VFX / композитинг** — EXR 32-bit для Nuke, DaVinci Resolve, Blender compositor
- **Архивирование** — храните мастера с полными данными, экспортируйте в любой формат позже

---

## Roadmap

- [ ] Выбор папки через параметр ноды
- [ ] Опция сжатия LZW/ZIP для TIFF
- [ ] Встраивание EXIF/IPTC метаданных (для стоковых воркфлоу)
- [ ] Многослойный EXR с раздельными каналами R/G/B/A

---

## Автор

**Orakul Studio** — Chernihiv, Ukraine 🇺🇦  
Flux2 · ComfyUI · RTX 4090 · No quantization · No compromises

---

## Лицензия

MIT — используй, форкай, улучшай.


[Back to English / Наверх](#comfyui-orakul-svp)


