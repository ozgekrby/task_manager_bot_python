import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import init_db, add_task_db, complete_task_db, get_task_by_id_db, clear_tasks_table

class TestCompleteTask(unittest.TestCase):
    TEST_DB_NAME = "test_complete_tasks.db"

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
        self.incomplete_task_desc = "Tamamlanacak görev"
        self.incomplete_task_id = add_task_db(self.incomplete_task_desc, db_name=self.TEST_DB_NAME)

    def test_complete_existing_incomplete_task(self):
        """Var olan ve tamamlanmamış bir görevi tamamlamayı test eder."""
        result = complete_task_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        self.assertTrue(result, "Görev başarıyla tamamlanmış olmalı.")

        completed_task = get_task_by_id_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        self.assertIsNotNone(completed_task, "Tamamlanan görev veritabanında bulunmalı.")
        self.assertEqual(completed_task[2], 1, "Görevin tamamlanma durumu '1' olmalı.")

    def test_complete_non_existing_task(self):
        """Var olmayan bir görevi tamamlamaya çalışmayı test eder."""
        non_existing_id = 999
        result = complete_task_db(non_existing_id, db_name=self.TEST_DB_NAME)
        self.assertFalse(result, "Var olmayan bir görev tamamlanamamalı.")

    def test_complete_already_completed_task(self):
        """Zaten tamamlanmış bir görevi tekrar tamamlamaya çalışmayı test eder."""
        complete_task_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        result = complete_task_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        self.assertFalse(result, "Zaten tamamlanmış bir görev tekrar tamamlanmaya çalışıldığında False dönmeli.")
        task_after_reattempt = get_task_by_id_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        self.assertEqual(task_after_reattempt[2], 1, "Görev hala tamamlanmış durumda olmalı.")

if __name__ == '__main__':
    unittest.main()