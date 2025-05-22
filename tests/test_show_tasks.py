import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import init_db, add_task_db, get_tasks_db, complete_task_db, clear_tasks_table

class TestShowTasks(unittest.TestCase):
    TEST_DB_NAME = "test_show_tasks.db"

    @classmethod
    def setUpClass(cls):
        if os.path.exists(cls.TEST_DB_NAME):
            os.remove(cls.TEST_DB_NAME)
        init_db(db_name=cls.TEST_DB_NAME)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.TEST_DB_NAME):
            os.remove(cls.TEST_DB_NAME)

    def setUp(self):
        clear_tasks_table(db_name=self.TEST_DB_NAME)

    def test_show_no_tasks(self):
        """Hiç görev olmadığında boş liste dönmesini test eder."""
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 0, "Hiç görev yokken boş liste dönmeli.")
        self.assertListEqual(tasks, [], "Hiç görev yokken boş liste dönmeli.")

    def test_show_one_incomplete_task(self):
        """Bir adet tamamlanmamış görev olduğunda doğru listelemeyi test eder."""
        desc = "Tek görev"
        task_id = add_task_db(desc, db_name=self.TEST_DB_NAME)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1, "Bir görev varken listede bir eleman olmalı.")
        
        expected_task = (task_id, desc, 0)
        self.assertEqual(tasks[0], expected_task, "Görevin bilgileri doğru olmalı.")

    def test_show_multiple_tasks_mixed_status(self):
        """Birden fazla görev (tamamlanmış ve tamamlanmamış) olduğunda doğru listelemeyi test eder."""
        desc1 = "İlk görev (tamamlanmamış)"
        id1 = add_task_db(desc1, db_name=self.TEST_DB_NAME)

        desc2 = "İkinci görev (tamamlanmış)"
        id2 = add_task_db(desc2, db_name=self.TEST_DB_NAME)
        complete_task_db(id2, db_name=self.TEST_DB_NAME)

        desc3 = "Üçüncü görev (tamamlanmamış)"
        id3 = add_task_db(desc3, db_name=self.TEST_DB_NAME)

        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 3, "Listede üç görev olmalı.")

        expected_tasks_data = [
            (id1, desc1, 0),
            (id2, desc2, 1),
            (id3, desc3, 0)
        ]
  
        actual_tasks_data = [(task[0], task[1], task[2]) for task in tasks]
        
        self.assertListEqual(actual_tasks_data, expected_tasks_data, "Görev listesi ve durumları doğru olmalı.")

    def test_show_one_completed_task(self):
        """Bir adet tamamlanmış görev olduğunda doğru listelemeyi test eder."""
        desc = "Tamamlanmış görev"
        task_id = add_task_db(desc, db_name=self.TEST_DB_NAME)
        complete_task_db(task_id, db_name=self.TEST_DB_NAME)

        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1, "Bir görev varken listede bir eleman olmalı.")

        expected_task = (task_id, desc, 1)
        self.assertEqual(tasks[0], expected_task, "Tamamlanmış görevin bilgileri doğru olmalı.")


if __name__ == '__main__':
    unittest.main()