import unittest
from parser import login_and_get_users_rows


class PhpMyAdminTests(unittest.TestCase):

    def test_login_successful(self):
        """Тест: успешная авторизация"""
        try:
            rows = login_and_get_users_rows()
            self.assertIsInstance(rows, list)
        except Exception as e:
            self.fail(f'Авторизация или загрузка таблицы не удалась: {e}')

    def test_users_table_not_empty(self):
        """Тест: таблица users не пуста"""
        rows = login_and_get_users_rows()
        self.assertGreater(len(rows), 0, 'Таблица users пуста')

    def test_row_structure(self):
        """Тест: каждая строка содержит хотя бы одну ячейку"""
        rows = login_and_get_users_rows()
        for row in rows:
            cols = row.select('td')
            self.assertGreater(len(cols), 0, 'В строке нет ячеек <td>')


if __name__ == '__main__':
    unittest.main()
