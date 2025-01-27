import os
import argparse
import arch_func

if __name__ == "__main__":

    # продумать текст
    # написать в хелпе пример использования
    parser = argparse.ArgumentParser(description='Утилита для архивирования и анализа файлов и папок')
    parser.add_argument('operation', help='archive для архивации папки, analyse для анализа папки')
    parser.add_argument('--sf', help='source folder путь к папке, которую хотите архивировать или анализировать')
    parser.add_argument('--df',
                        help='(опционально) destination folder путь к zip файлу (по умолчанию zip файл создастся в директории с утилитой)')

    args = parser.parse_args()

    if args.operation == 'archive':
        if not os.path.isdir(str(args.sf)):
            print("Укажите корректный путь к папке, которую хотите архивировать")
            exit(1)
        arch_func.folder_to_zip(args.sf, args.df)
    elif args.operation == 'analyse':
        if not os.path.isdir(str(args.sf)):
            print("Укажите корректный путь к папке, которую хотите анализировать")
            exit(1)
        arch_func.analyze_path(args.sf)
    else:
        print("Укажите корректную команду")
        exit(1)
