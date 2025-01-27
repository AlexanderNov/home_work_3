import unittest
import main
import arch_func


class TestArchiver(unittest.TestCase):
    def setUp(self):
        # создание и генерация файлов
        pass

    def tearDown(self):
        # удаление файлов
        pass

    def test_human_readable_size(self):
        """Проверка того, что введенное значение в байтах правильно переводится в байты, килобайты, мегабайты, гигабайты и терабайты"""
        self.assertEqual('0B', arch_func.human_readable_size(0))
        self.assertEqual('100B', arch_func.human_readable_size(100))
        self.assertEqual('3.15KB', arch_func.human_readable_size(1024 * 3 + 150))
        self.assertEqual('2.00MB', arch_func.human_readable_size(1024 * 1024 * 2))
        self.assertEqual('2.00GB', arch_func.human_readable_size(1024 * 1024 * 1024 * 2))
        self.assertEqual('2.00TB', arch_func.human_readable_size(1024 * 1024 * 1024 * 1024 * 2))
