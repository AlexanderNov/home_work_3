import os
import zipfile
from datetime import datetime


def folder_to_zip(source_folder, destination_folder):
    """
    Архивирует папку source_folder в папку destination_folder, выводит количество заархивированных файлов, выводит путь к получившемуся zip файлу
    """
    if destination_folder is None:
        destination_folder = os.getcwd() + "\\"
    elif not destination_folder.endswith("\\"):
        destination_folder += "\\"

    if not os.path.exists(destination_folder):
        raise ValueError("Укажите корректный путь к папке в которую хотите положить архив")

    destination_path = os.path.join(destination_folder, datetime.now().strftime('%Y-%m-%d-%H-%M') + '.zip')

    ui_archive_result = []
    files_count = 0
    try:
        with zipfile.ZipFile(destination_path, 'w') as zip_me:
            for folder, subfolders, files in os.walk(source_folder):
                for file in files:
                    zip_me.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), source_folder),
                                 compress_type=zipfile.ZIP_DEFLATED)
                    files_count += 1

        print(f"Количество заархивированных файлов: {files_count}")
        print(f"Файл архива: {destination_path}")
        ui_archive_result.append("Количество заархивированных файлов: " + str(files_count))
        ui_archive_result.append("Файл архива: " + destination_path)
    except PermissionError as e:
        ui_archive_result.append(f"Ошибка: {e}")
        print(f"Ошибка: {e}")
        raise
    finally:
        return ui_archive_result


def get_size(source_folder):
    """
    Высчитывает размер указанной папки
    """
    total_size = 0
    for folder, subfolders, files in os.walk(source_folder):
        for file in files:
            fp = os.path.join(folder, file)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def human_readable_size(size_bytes):
    """
    Преобразует переданное значение в B, KB, MB, GB, TB в зависимости от размера
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(size_bytes)
    grade = 0
    while i >= 1000:
        i /= 1024
        grade += 1
    if grade > 0:
        return f"{i:.2f}{size_name[grade]}"
    else:
        return f"{i:.0f}{size_name[grade]}"


def analyse_path(source_folder):
    """
    Выводит список папок и файлов с соответствующими размерами
    """
    ui_analyse_result = []
    print("full size:", human_readable_size(get_size(source_folder)))
    ui_analyse_result.append("full size: " + human_readable_size(get_size(source_folder)))

    try:
        for item in sorted(os.listdir(source_folder)):
            item_path = os.path.join(source_folder, item)
            if os.path.isdir(item_path):
                print(f"- {item}: {human_readable_size(get_size(item_path))}")
                ui_analyse_result.append("- " + item + ": " + human_readable_size(get_size(item_path)))
            else:
                print(f"- {item}: {human_readable_size(os.path.getsize(item_path))}")
                ui_analyse_result.append("- " + item + ": " + human_readable_size(os.path.getsize(item_path)))
    except PermissionError as e:
        ui_analyse_result.append(f"Ошибка: {e}")
        print(f"Ошибка: {e}")
        raise
    finally:
        return ui_analyse_result
