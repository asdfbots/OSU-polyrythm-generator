import subprocess
import os
import tempfile
import shutil

def poly_audio(audio_path, output, step_sec, changes):
    # Запоминаем абсолютный путь вывода
    output_abs = os.path.abspath(output)
    
    # Создаем скрытую временную папку для работы с кусочками
    temp_dir = tempfile.mkdtemp()
    
    try:
        print("1/3 Подготовка: конвертируем в WAV для идеальной точности (1 сек)...")
        full_wav = os.path.join(temp_dir, "TombstoneGypsyBardRemix-Final.mp3")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", audio_path, full_wav], check=True)
        
        # Получаем реальную длину
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", full_wav],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        duration = float(result.stdout.strip()) - 0.1  # -0.1 сек для защиты от "битого" хвоста файла
        
        valid_segments = []
        concat_list_path = os.path.join(temp_dir, "concat.txt")
        
        print(f"2/3 Нарезаем {len(changes)} сегментов (это займет 5-15 секунд)...")
        
        for i, coeff in enumerate(changes):
            start = i * step_sec
            if start >= duration:
                break
                
            end = min((i + 1) * step_sec, duration)
            if end - start < 0.005:
                break
                
            coeff = max(0.5, min(2.0, coeff))
            
            # Генерируем имена: seg_0000.wav, seg_0001.wav ...
            seg_filename = f"seg_{i:04d}.wav"
            seg_filepath = os.path.join(temp_dir, seg_filename)
            
            # Поскольку мы режем WAV, это происходит мгновенно
            cmd = [
                "ffmpeg", "-y", "-v", "error",
                "-ss", str(start),
                "-t", str(end - start),
                "-i", full_wav
            ]
            
            if abs(coeff - 1.0) >= 1e-5:
                cmd.extend(["-af", f"asetrate={44100*coeff},aresample=44100"])
                
            cmd.append(seg_filepath)
            subprocess.run(cmd, check=True)
            valid_segments.append(seg_filename)
            
        print("3/3 Склеиваем всё обратно в MP3...")
        # Записываем текстовый список файлов для склейки
        with open(concat_list_path, "w", encoding="utf-8") as f:
            for seg in valid_segments:
                f.write(f"file '{seg}'\n")
                
        # Склеиваем! Запускаем команду прямо внутри временной папки
        concat_cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-f", "concat",
            "-safe", "0",
            "-i", "concat.txt",
            output_abs
        ]
        subprocess.run(concat_cmd, cwd=temp_dir, check=True)
        
        print(f"\n✅ Успех! Полиритм сохранен в файл: {output}")
        
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
    finally:
        # В самом конце удаляем временную папку и все 233 нарезанных файлика
        shutil.rmtree(temp_dir, ignore_errors=True)

# Ваш список:
inp = [1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0, 2.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 1.0, 2.0, 1.0]
poly_audio("metronome.mp3", "polynome.mp3", 2, inp)