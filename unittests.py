import unittest
import os
import zipfile
import io
from archfunc import folder_to_zip, get_size, human_readable_size, analyse_path
from unittest.mock import patch


class TestArchiveAndAnalyse(unittest.TestCase):
    def setUp(self):
        """Подготовка тестовой папки с файлами"""
        self.test_folder = "test_folder"
        os.makedirs(self.test_folder, exist_ok=True)
        with open(os.path.join(self.test_folder, "file1.txt"), "w") as f:
            f.write("Test file 1")
        with open(os.path.join(self.test_folder, "file2.txt"), "w") as f:
            f.write("Test file 2")

    def tearDown(self):
        """Удаление тестовой папки с файлами"""
        for root, dirs, files in os.walk(self.test_folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_folder)

    def test_folder_to_zip(self):
        """Тестирование архивации"""
        # Создаем архив
        destination_folder = "."
        folder_to_zip(self.test_folder, destination_folder)

        # Проверяем, что архив создан и файл не нулевой
        zip_files = [f for f in os.listdir(destination_folder) if f.endswith('.zip')]
        self.assertTrue(len(zip_files) > 0)

        # Проверяем, что содержимое архива соответствует папке, которую архивировали
        with zipfile.ZipFile(zip_files[0], 'r') as zip_ref:
            zip_ref.extractall("extracted")
            self.assertTrue(os.path.exists("extracted/file1.txt"))
            self.assertTrue(os.path.exists("extracted/file2.txt"))

        # Удаляем временные файлы
        os.remove(zip_files[0])
        os.remove("extracted/file1.txt")
        os.remove("extracted/file2.txt")
        os.rmdir("extracted")

    def test_get_size(self):
        """Тестирование подсчета размера папки"""
        size = get_size(self.test_folder)
        self.assertEqual(size, 22)  # 11 байт на каждый файл

    def test_analyse_path(self):
        # Ожидаемый вывод функции analyse_path
        expected_output = [
            f"full size: {human_readable_size(get_size(self.test_folder))}",
            f"- file1.txt: {human_readable_size(os.path.getsize(os.path.join(self.test_folder, 'file1.txt')))}",
            f"- file2.txt: {human_readable_size(os.path.getsize(os.path.join(self.test_folder, 'file2.txt')))}",
        ]

        # Захватываем вывод функции analyse_path
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            analyse_path(self.test_folder)
            # Получаем вывод
            captured_output = mock_stdout.getvalue().strip().split("\n")

        # Проверяем, что вывод соответствует ожидаемому
        self.assertEqual(len(captured_output), len(expected_output))
        for expected, actual in zip(expected_output, captured_output):
            self.assertIn(expected, actual)


class TestHumanReadableSize(unittest.TestCase):

    def test_human_readable_size(self):
        """Проверка того, что введенное значение в байтах правильно переводится в байты, килобайты, мегабайты, гигабайты и терабайты"""
        self.assertEqual('0B', human_readable_size(0))
        self.assertEqual('100B', human_readable_size(100))
        self.assertEqual('3.15KB', human_readable_size(1024 * 3 + 150))
        self.assertEqual('2.00MB', human_readable_size(1024 * 1024 * 2))
        self.assertEqual('2.00GB', human_readable_size(1024 * 1024 * 1024 * 2))
        self.assertEqual('2.00TB', human_readable_size(1024 * 1024 * 1024 * 1024 * 2))
