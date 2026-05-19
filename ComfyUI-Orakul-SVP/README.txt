
https://github.com/OrakulStudio

=== ORAKUL STUDIO ENGINE v2.0 ===

This folder contains TWO custom nodes for ComfyUI. They work together as a powerful hybrid system for master-grade rendering (TIFF 16-bit / EXR 32-bit).

1. orakul_svp_node.py (OrakulSVPNode)
   - What it does: This is the automated rendering core. Connect it directly after your VAE Decoder.
   - Purpose: It instantly dumps your raw image generation from VRAM to disk inside "output/temp_svp/".

2. orakul_injector.py (OrakulMetadataInjector)
   - What it does: This is the manual firmware injector node. It has a custom "Play" button in the menu.
   - Purpose: Place it anywhere in your workflow. When your batch generation is fully done, click "Play" on this node to immediately inject your full ComfyUI JSON-workflow metadata directly into the saved TIFF/EXR files.

QUICK START:
1. Put both files into your "ComfyUI/custom_nodes/Orakul_Studio/" folder.

2. Restart ComfyUI.

3. Add "OrakulSVPNode" to stream the frames.

4. Add "OrakulMetadataInjector" to sign your master files via Execute/Play.



https://github.com/OrakulStudio

=== ORAKUL STUDIO ENGINE v2.0 ===   

Эта папка содержит ДВА пользовательских узла для ComfyUI. Они работают вместе как мощная гибридная система для рендеринга мастер-класса (TIFF 16-бит / EXR 32-бит).

1. orakul_svp_node.py (OrakulSVPNode)
- Что он делает: Это ядро ​​автоматического рендеринга. Подключите его напрямую после вашего VAE-декодера.

- Назначение: Мгновенно выгружает сгенерированное вами необработанное изображение из VRAM на диск в папку "output/temp_svp/".

2. orakul_injector.py (OrakulMetadataInjector)
- Что он делает: Это узел ручного внедрения прошивки. Он имеет пользовательскую кнопку "Play" в меню.

- Назначение: Разместите его в любом месте вашего рабочего процесса. Когда генерация пакета завершится, нажмите кнопку «Воспроизвести» на этом узле, чтобы немедленно внедрить все метаданные рабочего процесса ComfyUI в формате JSON непосредственно в сохраненные файлы TIFF/EXR.

БЫСТРЫЙ СТАРТ:
1. Поместите оба файла в папку «ComfyUI/custom_nodes/Orakul_Studio/».

2. Перезапустите ComfyUI.

3. Добавьте «OrakulSVPNode» для потоковой передачи кадров.

4. Добавьте «OrakulMetadataInjector» для подписи ваших мастер-файлов через Execute/Play.