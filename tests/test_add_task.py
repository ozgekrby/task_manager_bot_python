import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import init_db, add_task_db, get_tasks_db, clear_tasks_table

class TestAddTask(unittest.TestCase):
    TEST_DB_NAME = "test_add_tasks.db"

    @classmethod
    def setUpClass(cls):
        """Bu sınıftaki tüm testlerden önce bir kez çalışır."""
        if os.path.exists(cls.TEST_DB_NAME):
            os.remove(cls.TEST_DB_NAME)
        init_db(db_name=cls.TEST_DB_NAME)

    @classmethod
    def tearDownClass(cls):
        """Bu sınıftaki tüm testlerden sonra bir kez çalışır."""
        if os.path.exists(cls.TEST_DB_NAME):
            os.remove(cls.TEST_DB_NAME)

    def setUp(self):
        """Her test metodundan önce çalışır."""
        clear_tasks_table(db_name=self.TEST_DB_NAME)

    def test_add_single_task(self):
        description = "Test için ilk görev"
        task_id = add_task_db(description, db_name=self.TEST_DB_NAME)
        self.assertIsNotNone(task_id, "Görev ID'si None olmamalı.")
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1, "Veritabanında bir görev olmalı.")
        self.assertEqual(tasks[0][1], description, "Görev açıklaması eşleşmeli.")
        self.assertEqual(tasks[0][2], 0, "Görev tamamlanmamış olmalı.")

    def test_add_multiple_tasks(self):
        add_task_db("Görev 1", db_name=self.TEST_DB_NAME)
        add_task_db("Görev 2", db_name=self.TEST_DB_NAME)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 2, "Veritabanında iki görev olmalı.")

if __name__ == '__main__':
    unittest.main()