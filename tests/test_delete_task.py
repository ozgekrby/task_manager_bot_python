import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import init_db, add_task_db, delete_task_db, get_tasks_db, clear_tasks_table

class TestDeleteTask(unittest.TestCase):
    TEST_DB_NAME = "test_delete_tasks.db"

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
        self.task_id_to_delete = add_task_db("Silinecek görev", db_name=self.TEST_DB_NAME)
        add_task_db("Silinmeyecek görev", db_name=self.TEST_DB_NAME)

    def test_delete_existing_task(self):
        initial_tasks = get_tasks_db(db_name=self.TEST_DB_NAME)

        result = delete_task_db(self.task_id_to_delete, db_name=self.TEST_DB_NAME)
        self.assertTrue(result, "Var olan görev silinebilmeli.")
        
        tasks_after_delete = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks_after_delete), 1, "Bir görev silindikten sonra bir görev kalmalı.")
        self.assertNotEqual(tasks_after_delete[0][0], self.task_id_to_delete, "Kalan görev silinen görev olmamalı.")

    def test_delete_non_existing_task(self):
        initial_tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        
        non_existing_id = 9999
        result = delete_task_db(non_existing_id, db_name=self.TEST_DB_NAME)
        self.assertFalse(result, "Var olmayan görev silinememeli.")
        
        tasks_after_attempted_delete = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks_after_attempted_delete), 2, "Var olmayan bir görev silinmeye çalışıldığında görev sayısı değişmemeli.")

if __name__ == '__main__':
    unittest.main()