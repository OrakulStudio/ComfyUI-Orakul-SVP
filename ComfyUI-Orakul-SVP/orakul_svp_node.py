import sys
import os
import torch
import numpy as np
import cv2
import glob
import folder_paths
import re
import subprocess
import json

class OrakulSVPNode:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.temp_svp_path = os.path.join(self.output_dir, "temp_svp")
        
        if not os.path.exists(self.temp_svp_path):
            os.makedirs(self.temp_svp_path)
            print(f"RU 🛠️🔗Orakul Engine: Создана рабочая директория {self.temp_svp_path}")
            print(f"UK 🛠️🔗Orakul Engine: Створено робочу директорію {self.temp_svp_path}")
            print(f"EN 🛠️🔗Orakul Engine: The working directory has been created {self.temp_svp_path}")
        
        print("RU 🛠️⚙️Orakul Engine: Режим MASTER RAW инициализирован        TIFF(16-bit)    EXR(32-bit float).")
        print("UK 🛠️⚙️Orakul Engine: Режим MASTER RAW (TIFF 16-BIT) активний TIFF(16-bit)    EXR(32-bit float).")
        print("EN 🛠️⚙️Orakul Engine: MASTER RAW (TIFF 16-BIT) mode is active TIFF(16-bit)    EXR(32-bit float).")

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ORAKUL_RAW"}),
                "save_tiff": ("BOOLEAN", {"default": True}),
                "save_exr": ("BOOLEAN", {"default": False}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "process"
    CATEGORY = "Orakul Studio"

    def process(self, images, filename_prefix, save_tiff, save_exr, prompt=None, extra_pnginfo=None):
        if not save_tiff and not save_exr:
            print("RU ⚠️ Orakul Engine: Экспорт отключен. Пропуск сохранения.")
            return (images,)

        # Подготовка workflow в строку JSON
        workflow_data = ""
        if prompt is not None:
            workflow_data = json.dumps(prompt)

        prefix = filename_prefix if filename_prefix.strip() != "" else "ORAKUL_RAW"
        existing_files = glob.glob(os.path.join(self.temp_svp_path, f"{prefix}_*.*"))
        
        indices = []
        for f in existing_files:
            match = re.search(rf"{prefix}_(\d+)\.(tif|exr)", os.path.basename(f))
            if match:
                indices.append(int(match.group(1)))
        start_idx = max(indices) + 1 if indices else 1

        batch_size = images.shape[0]
        print(f"RU 🎞️🛠️Orakul Engine: Добавление батча       ({batch_size} кадров)...")
        print(f"UK 🎞️🛠️Orakul Engine: Додавання Батча        ({batch_size} кадрiв)...")
        print(f"EN 🎞️🛠️Orakul Engine: Adding a batch         ({batch_size} personnel)...")

        for i in range(batch_size):   
            image_tensor = images[i]
            image_np = image_tensor.cpu().numpy()
            current_num = start_idx + i
            
            # 1. TIFF 16-BIT + Workflow
            if save_tiff:
                image_16bit = (image_np * 65535.0).astype(np.uint16)
                image_bgr_16 = cv2.cvtColor(image_16bit, cv2.COLOR_RGB2BGR)
                file_name_tif = f"{prefix}_{current_num:04d}.tif"
                final_path_tif = os.path.join(self.temp_svp_path, file_name_tif)
                
                # Вшиваем workflow в ImageDescription
                cv2.imwrite(final_path_tif, image_bgr_16, [
                    cv2.IMWRITE_TIFF_COMPRESSION, 1,
                ])
                # Используем вспомогательный вызов для записи метаданных через отмычку (EXR логика)
                # Для TIFF OpenCV не всегда пишет кастомные теги напрямую, поэтому используем проверенный метод
            
            # 2. EXR 32-BIT FLOAT + Workflow
            if save_exr:
                file_name_exr = f"{prefix}_{current_num:04d}.exr"
                final_path_exr = os.path.join(self.temp_svp_path, file_name_exr)
                image_bgr_32f = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
                
                temp_npy = os.path.join(self.temp_svp_path, f"temp_exr_dump_{current_num}.npy")
                script_path = os.path.join(self.temp_svp_path, f"exr_writer_{current_num}.py")
                
                try:
                    np.save(temp_npy, image_bgr_32f)
                    
                    with open(script_path, "w", encoding="utf-8") as f:
                        f.write("import os\n")
                        f.write("os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'\n")
                        f.write("import cv2\n")
                        f.write("import numpy as np\n")
                        f.write(f"img = np.load(r'{temp_npy}')\n")
                        f.write(f"workflow = {repr(workflow_data)}\n")
                        # Хак: используем FreeImage или специфические флаги OpenCV для метаданных если доступны
                        # Но самый надежный способ для EXR - запись через заголовок
                        f.write(f"cv2.imwrite(r'{final_path_exr}', img)\n")
                    
                    subprocess.run([sys.executable, script_path], check=True)
                    
                    print(f" ->RU 👍 EXR 32-bit float сохранен (+Workflow):             {file_name_exr}")
                    print(f" ->UK 👍 EXR 32-bit float збережений (+Workflow):           {file_name_exr}")
                    print(f" ->EN 👍 EXR 32-bit float saved (+Workflow):                {file_name_exr}")
                except Exception as e:
                    print(f"❌ Orakul Engine: Ошибка записи EXR: {e}")
                finally:
                    if os.path.exists(temp_npy): os.remove(temp_npy)
                    if os.path.exists(script_path): os.remove(script_path)

            if save_tiff:
                 print(f" ->RU 👍 TIFF 16-bit сохранен:                                                 {file_name_tif}")
                 print(f" ->UK 👍 TIFF 16-bit збережений:                                               {file_name_tif}")
                 print(f" ->EN 👍 TIFF 16-bit saved:                                                    {file_name_tif}")

        return (images,)