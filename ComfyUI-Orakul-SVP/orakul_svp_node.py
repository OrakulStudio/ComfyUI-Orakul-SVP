import torch
import numpy as np
import os
import cv2
import glob
import folder_paths
import re

class OrakulSVPNode:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.temp_svp_path = os.path.join(self.output_dir, "temp_svp")
        
        # Просто создаем папку, если её нет. Старые файлы не трогаем.
        if not os.path.exists(self.temp_svp_path):
            os.makedirs(self.temp_svp_path)
            print(f"🛠️🔗Orakul Engine: Создана рабочая директория {self.temp_svp_path}")
            print(f"🛠️🔗Orakul Engine: Створено робочу директорію {self.temp_svp_path}")
            print(f"🛠️🔗Orakul Engine: The working directory has been created {self.temp_svp_path}")
        
        print("🛠️⚙️Orakul Engine: Режим MASTER RAW (TIFF 16-BIT) активен. Режим накопления.")
        print("🛠️⚙️Orakul Engine: Режим MASTER RAW (TIFF 16-BIT) активний. Режим накопичення.")
        print("🛠️⚙️Orakul Engine: MASTER RAW (TIFF 16-BIT) mode is active. Accumulation mode.")

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "process"
    CATEGORY = "Orakul Studio"

    def process(self, images):
        if not os.path.exists(self.temp_svp_path):
            os.makedirs(self.temp_svp_path)

        # 1. Считаем, какой индекс должен быть следующим
        existing_files = glob.glob(os.path.join(self.temp_svp_path, "ORAKUL_RAW_*.tif"))
        
        if not existing_files:
            start_idx = 1
        else:
            # Извлекаем числа из названий и находим максимум
            indices = []
            for f in existing_files:
                match = re.search(r"ORAKUL_RAW_(\d+)\.tif", os.path.basename(f))
                if match:
                    indices.append(int(match.group(1)))
            start_idx = max(indices) + 1 if indices else 1

        batch_size = images.shape[0]
        print(f"🎞️🛠️Orakul Engine: Додавання Батча ({batch_size} кадрів) до існуючих...")
        print(f"🎞️🛠️Orakul Engine: Добавление батча ({batch_size} кадров) к существующим...")
        print(f"🎞️🛠️Orakul Engine: Adding a Batch ({batch_size} personnel) to existing ones...")

        for i in range(batch_size):
            image_tensor = images[i]
            image_np = image_tensor.cpu().numpy()
            image_16bit = (image_np * 65535.0).astype(np.uint16)
            image_bgr_16 = cv2.cvtColor(image_16bit, cv2.COLOR_RGB2BGR)

            # Используем сквозную нумерацию
            current_num = start_idx + i
            file_name = f"ORAKUL_RAW_{current_num:04d}.tif"
            final_path = os.path.join(self.temp_svp_path, file_name)

            cv2.imwrite(final_path, image_bgr_16, [cv2.IMWRITE_TIFF_COMPRESSION, 1])
            
            print(f" -> 👍Добавлено: {file_name}")
            print(f" -> 👍Added: {file_name}")
            print(f" -> 👍Додано: {file_name}")

        return (images,)