import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import init_db, add_task_db, complete_task_db, get_task_by_id_db, clear_tasks_table

class TestCompleteTask(unittest.TestCase):
    TEST_DB_NAME = "test_complete_tasks.db"

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
        self.incomplete_task_desc = "Task to complete"
        self.incomplete_task_id = add_task_db(self.incomplete_task_desc, db_name=self.TEST_DB_NAME)

    def test_complete_existing_incomplete_task(self):
        result = complete_task_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        self.assertTrue(result, "Task should be marked as completed successfully.")

        completed_task = get_task_by_id_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        self.assertIsNotNone(completed_task, "Completed task should be found in the database.")
        self.assertEqual(completed_task[2], 1, "Task status should be '1' (completed).")

    def test_complete_non_existing_task(self):
        non_existing_id = 999
        result = complete_task_db(non_existing_id, db_name=self.TEST_DB_NAME)
        self.assertFalse(result, "Non-existing task should not be marked as completed.")

    def test_complete_already_completed_task(self):
        complete_task_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        result = complete_task_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        self.assertFalse(result, "Already completed task should return False when trying to complete again.")
        task_after_reattempt = get_task_by_id_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        self.assertEqual(task_after_reattempt[2], 1, "Task should still be completed.")

    def test_complete_negative_task_id(self):
        result = complete_task_db(-1, db_name=self.TEST_DB_NAME)
        self.assertFalse(result)

    def test_complete_zero_task_id(self):
        result = complete_task_db(0, db_name=self.TEST_DB_NAME)
        self.assertFalse(result)

    def test_complete_very_large_task_id(self):
        result = complete_task_db(999999999, db_name=self.TEST_DB_NAME)
        self.assertFalse(result)

    def test_complete_multiple_tasks_sequentially(self):
        task1_id = add_task_db("Task 1", db_name=self.TEST_DB_NAME)
        task2_id = add_task_db("Task 2", db_name=self.TEST_DB_NAME)
        task3_id = add_task_db("Task 3", db_name=self.TEST_DB_NAME)
        
        self.assertTrue(complete_task_db(task1_id, db_name=self.TEST_DB_NAME))
        self.assertTrue(complete_task_db(task2_id, db_name=self.TEST_DB_NAME))
        self.assertTrue(complete_task_db(task3_id, db_name=self.TEST_DB_NAME))
        
        task1 = get_task_by_id_db(task1_id, db_name=self.TEST_DB_NAME)
        task2 = get_task_by_id_db(task2_id, db_name=self.TEST_DB_NAME)
        task3 = get_task_by_id_db(task3_id, db_name=self.TEST_DB_NAME)
        
        self.assertEqual(task1[2], 1)
        self.assertEqual(task2[2], 1)
        self.assertEqual(task3[2], 1)

    def test_complete_task_preserves_description(self):
        original_task = get_task_by_id_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        original_description = original_task[1]
        
        complete_task_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        
        completed_task = get_task_by_id_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        self.assertEqual(completed_task[1], original_description)

    def test_complete_task_preserves_id(self):
        original_task = get_task_by_id_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        original_id = original_task[0]
        
        complete_task_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        
        completed_task = get_task_by_id_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        self.assertEqual(completed_task[0], original_id)

    def test_complete_task_multiple_attempts_same_result(self):
        result1 = complete_task_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        result2 = complete_task_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        result3 = complete_task_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        
        self.assertTrue(result1)
        self.assertFalse(result2)
        self.assertFalse(result3)

    def test_complete_task_with_special_characters(self):
        special_task_id = add_task_db("Task with !@#$%^&*()", db_name=self.TEST_DB_NAME)
        result = complete_task_db(special_task_id, db_name=self.TEST_DB_NAME)
        self.assertTrue(result)
        
        completed_task = get_task_by_id_db(special_task_id, db_name=self.TEST_DB_NAME)
        self.assertEqual(completed_task[2], 1)

    def test_complete_task_with_unicode(self):
        unicode_task_id = add_task_db("Task with émojis 🎉", db_name=self.TEST_DB_NAME)
        result = complete_task_db(unicode_task_id, db_name=self.TEST_DB_NAME)
        self.assertTrue(result)
        
        completed_task = get_task_by_id_db(unicode_task_id, db_name=self.TEST_DB_NAME)
        self.assertEqual(completed_task[2], 1)

    def test_complete_task_after_delete_and_recreate(self):
        complete_task_db(self.incomplete_task_id, db_name=self.TEST_DB_NAME)
        
        clear_tasks_table(db_name=self.TEST_DB_NAME)
        new_task_id = add_task_db("New task", db_name=self.TEST_DB_NAME)
        
        result = complete_task_db(new_task_id, db_name=self.TEST_DB_NAME)
        self.assertTrue(result)

    def test_complete_task_with_print(self):
        print("Testing complete_task() function.")
        print("Database connection is initialized.")
        clear_tasks_table(db_name=self.TEST_DB_NAME)
        print("Adding a task to the database.")
        desc = "Task to complete"
        task_id = add_task_db(desc, db_name=self.TEST_DB_NAME)
        print(f"Task added with id {task_id}.")
        print("Completing the task.")
        result = complete_task_db(task_id, db_name=self.TEST_DB_NAME)
        if result:
            print("Test passed: Task marked as completed.")
        else:
            print("Test failed: Task could not be marked as completed.")
        task = get_task_by_id_db(task_id, db_name=self.TEST_DB_NAME)
        if task and task[2] == 1:
            print("Test passed: Task status is completed in the database.")
        else:
            print("Test failed: Task status is not completed in the database.")
        self.assertTrue(result)
        self.assertEqual(task[2], 1)

if __name__ == '__main__':
    unittest.main()