# ComfyUI-Orakul-SVP

**Dual Export Node for ComfyUI — PNG to /output + 16-bit RAW TIFF to /output/temp_svp**

> Простое решение для сохранения результатов генерации в двух форматах одновременно:  
> стандартный PNG в папку ComfyUI `/output` и архивный 16-bit TIFF без сжатия в `/output/temp_svp`.  
> Поддерживает batch, накопительный режим и сквозную нумерацию файлов.

---

## Зачем это нужно

ComfyUI по умолчанию сохраняет PNG в 8 бит. Для стоковой фотографии, печати и профессиональной постобработки этого недостаточно  теряется половина тонального диапазона.

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
