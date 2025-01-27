import os
import zipfile
from datetime import datetime
from logging import raiseExceptions


def folder_to_zip(source_folder, destination_folder=os.getcwd()):
    files_count = 0
    if destination_folder is None:
        destination_folder = os.getcwd() + "\\"
    elif not destination_folder.endswith("\\"):
        destination_folder = destination_folder + "\\"
    if not os.path.exists(destination_folder):
        print("Укажите корректный путь к папке в которую хотите положить архив")
        exit(1)

    zip_me = zipfile.ZipFile(destination_folder + datetime.now().strftime('%Y-%m-%d-%H-%M') + '.zip', 'w')
    for folder, subfolders, files in os.walk(source_folder):
        for file in files:
            zip_me.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), source_folder),
                         compress_type=zipfile.ZIP_DEFLATED)
            files_count += 1
    zip_me.close()

    print(f"Количество заархивированных файлов: {files_count}")


def get_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def human_readable_size(size_bytes):
    """
    Преобразует размер файла в KB, MB, GB в зависимости от размера
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(size_bytes / 1024)
    power = 0
    while i >= 1000:
        i /= 1024
        power += 1
    return f"{i:.2f}{size_name[power]}"


def analyze_path(path="."):
    print("full size:", human_readable_size(get_size(path)))
    for item in sorted(os.listdir(path)):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            print(f"- {item}: {human_readable_size(get_size(item_path))}")
        else:
            print(f"- {item}: {human_readable_size(os.path.getsize(item_path))}")
