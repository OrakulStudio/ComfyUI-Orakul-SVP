import os
import json
import glob
import folder_paths
import time  # Добавил для сброса кэша
from PIL import Image, TiffImagePlugin

class OrakulMetadataInjector:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.temp_svp_path = os.path.join(self.output_dir, "temp_svp")

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "info": ("STRING", {"default": "Нажми правой кнопкой -> Execute или кнопку Play"}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    # ГЛАВНЫЙ ФИКС: Эта штука заставляет сервер забыть про кэш
    @classmethod
    def IS_CHANGED(s, **kwargs):
        return time.time()

    RETURN_TYPES = ()
    FUNCTION = "inject"
    CATEGORY = "Orakul Studio"
    OUTPUT_NODE = True

    def inject(self, info, prompt=None, extra_pnginfo=None):
        output_dir = folder_paths.get_output_directory()
        temp_path = os.path.join(output_dir, "temp_svp")
        
        if not os.path.exists(temp_path):
            print(f"RU ❌ Orakul: Папка {temp_path} не найдена!")
            print(f"UK ❌ Orakul: Папка {temp_path} не знайдено!")
            print(f"EN ❌ Orakul: Папка {temp_path} not found!")
            return {}

        workflow_data = "{}"
        try:
            if extra_pnginfo is not None and "workflow" in extra_pnginfo:
                workflow_data = json.dumps(extra_pnginfo["workflow"])
            elif prompt is not None:
                workflow_data = json.dumps(prompt)
        except Exception as e:
            print(f"RU ⚠️ Ошибка сбора метаданных: {e}")
            print(f"UK ⚠️ Ошибка сбора метаданных: {e}")
            print(f"EN ⚠️ Metadata collection error: {e}")

        print(f"\nRU 💉⚙️ Orakul Injector: Запуск прошивки через Execute...")
        print(f"UK 💉⚙️ Orakul Injector: Запуск прошивки через Execute...")
        print(f"EN 💉⚙️ Orakul Injector: Launching firmware via Execute...")

        all_tiffs = glob.glob(os.path.join(temp_path, "*.tif"))
        for path in all_tiffs:
            try:
                img = Image.open(path)
                meta = TiffImagePlugin.ImageFileDirectory_v2()
                meta[270] = workflow_data
                meta[305] = "Orakul Master Engine"
                img.save(path, tiffinfo=meta)
                print(f"RU ✅ Подписан:  {os.path.basename(path)}")
                print(f"UK ✅ Підписано: {os.path.basename(path)}")
                print(f"EN ✅ Signed:    {os.path.basename(path)}")
            except Exception as e:
                print(f"RU ❌ Ошибка  TIFF {path}: {e}")
                print(f"UK ❌ Помилка TIFF {path}: {e}")
                print(f"EN ❌ Error   TIFF {path}: {e}")

        exr_files = glob.glob(os.path.join(temp_path, "*.exr"))
        if exr_files:
            json_path = os.path.join(temp_path, "batch_workflow.json")
            with open(json_path, "w", encoding="utf-8") as f:
                f.write(workflow_data)
            print(f"RU ✅ EXR Паспорт обновлен: {json_path}")
            print(f"UK ✅ EXR Паспорт оновлено: {json_path}")
            print(f"EN ✅ EXR Паспорт обновлен: {json_path}")
        
        print("RU 🏁 Готово! Метаданные впрыснуты.\n")
        print("UK 🏁 Готово! Метадані впорснуті.\n")
        print("EN 🏁 Ready!  Metadata injected.\n")
        
        return {}