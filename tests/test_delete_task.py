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
        self.task_id_to_delete = add_task_db("Task to delete", db_name=self.TEST_DB_NAME)
        add_task_db("Task to keep", db_name=self.TEST_DB_NAME)

    def test_delete_existing_task(self):
        initial_tasks = get_tasks_db(db_name=self.TEST_DB_NAME)

        result = delete_task_db(self.task_id_to_delete, db_name=self.TEST_DB_NAME)
        self.assertTrue(result, "Existing task should be deleted.")
        
        tasks_after_delete = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks_after_delete), 1, "There should be one task left after deletion.")
        self.assertNotEqual(tasks_after_delete[0][0], self.task_id_to_delete, "Remaining task should not be the deleted one.")

    def test_delete_non_existing_task(self):
        initial_tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        
        non_existing_id = 9999
        result = delete_task_db(non_existing_id, db_name=self.TEST_DB_NAME)
        self.assertFalse(result, "Non-existing task should not be deleted.")
        
        tasks_after_attempted_delete = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks_after_attempted_delete), 2, "Task count should not change when deleting non-existing task.")

    def test_delete_negative_task_id(self):
        result = delete_task_db(-1, db_name=self.TEST_DB_NAME)
        self.assertFalse(result)

    def test_delete_zero_task_id(self):
        result = delete_task_db(0, db_name=self.TEST_DB_NAME)
        self.assertFalse(result)

    def test_delete_very_large_task_id(self):
        result = delete_task_db(999999999, db_name=self.TEST_DB_NAME)
        self.assertFalse(result)

    def test_delete_completed_task(self):
        from database import complete_task_db
        complete_task_id = add_task_db("Completed task", db_name=self.TEST_DB_NAME)
        complete_task_db(complete_task_id, db_name=self.TEST_DB_NAME)
        
        result = delete_task_db(complete_task_id, db_name=self.TEST_DB_NAME)
        self.assertTrue(result)
        
        tasks_after_delete = get_tasks_db(db_name=self.TEST_DB_NAME)
        remaining_ids = [task[0] for task in tasks_after_delete]
        self.assertNotIn(complete_task_id, remaining_ids)

    def test_delete_multiple_tasks_sequentially(self):
        task1_id = add_task_db("Task 1", db_name=self.TEST_DB_NAME)
        task2_id = add_task_db("Task 2", db_name=self.TEST_DB_NAME)
        task3_id = add_task_db("Task 3", db_name=self.TEST_DB_NAME)
        
        self.assertTrue(delete_task_db(task1_id, db_name=self.TEST_DB_NAME))
        self.assertTrue(delete_task_db(task2_id, db_name=self.TEST_DB_NAME))
        self.assertTrue(delete_task_db(task3_id, db_name=self.TEST_DB_NAME))
        
        tasks_after_deletes = get_tasks_db(db_name=self.TEST_DB_NAME)
        remaining_ids = [task[0] for task in tasks_after_deletes]
        self.assertNotIn(task1_id, remaining_ids)
        self.assertNotIn(task2_id, remaining_ids)
        self.assertNotIn(task3_id, remaining_ids)

    def test_delete_all_tasks(self):
        all_tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        task_ids = [task[0] for task in all_tasks]
        
        for task_id in task_ids:
            self.assertTrue(delete_task_db(task_id, db_name=self.TEST_DB_NAME))
        
        remaining_tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(remaining_tasks), 0)

    def test_delete_task_with_special_characters(self):
        special_task_id = add_task_db("Task with !@#$%^&*()", db_name=self.TEST_DB_NAME)
        result = delete_task_db(special_task_id, db_name=self.TEST_DB_NAME)
        self.assertTrue(result)
        
        tasks_after_delete = get_tasks_db(db_name=self.TEST_DB_NAME)
        remaining_ids = [task[0] for task in tasks_after_delete]
        self.assertNotIn(special_task_id, remaining_ids)

    def test_delete_task_with_unicode(self):
        unicode_task_id = add_task_db("Task with émojis 🎉", db_name=self.TEST_DB_NAME)
        result = delete_task_db(unicode_task_id, db_name=self.TEST_DB_NAME)
        self.assertTrue(result)
        
        tasks_after_delete = get_tasks_db(db_name=self.TEST_DB_NAME)
        remaining_ids = [task[0] for task in tasks_after_delete]
        self.assertNotIn(unicode_task_id, remaining_ids)

    def test_delete_task_after_completion(self):
        from database import complete_task_db
        complete_task_db(self.task_id_to_delete, db_name=self.TEST_DB_NAME)
        
        result = delete_task_db(self.task_id_to_delete, db_name=self.TEST_DB_NAME)
        self.assertTrue(result)
        
        tasks_after_delete = get_tasks_db(db_name=self.TEST_DB_NAME)
        remaining_ids = [task[0] for task in tasks_after_delete]
        self.assertNotIn(self.task_id_to_delete, remaining_ids)

    def test_delete_task_idempotency(self):
        result1 = delete_task_db(self.task_id_to_delete, db_name=self.TEST_DB_NAME)
        result2 = delete_task_db(self.task_id_to_delete, db_name=self.TEST_DB_NAME)
        
        self.assertTrue(result1)
        self.assertFalse(result2)

    def test_delete_task_preserves_other_tasks(self):
        other_task_id = add_task_db("Task to keep", db_name=self.TEST_DB_NAME)
        
        delete_task_db(self.task_id_to_delete, db_name=self.TEST_DB_NAME)
        
        tasks_after_delete = get_tasks_db(db_name=self.TEST_DB_NAME)
        remaining_ids = [task[0] for task in tasks_after_delete]
        self.assertIn(other_task_id, remaining_ids)

    def test_delete_task_with_print(self):
        print("Testing delete_task() function.")
        print("Database connection is initialized.")
        clear_tasks_table(db_name=self.TEST_DB_NAME)
        print("Adding a task to the database.")
        desc = "Task to delete"
        task_id = add_task_db(desc, db_name=self.TEST_DB_NAME)
        print(f"Task added with id {task_id}.")
        print("Deleting the task.")
        result = delete_task_db(task_id, db_name=self.TEST_DB_NAME)
        if result:
            print("Test passed: Task deleted successfully.")
        else:
            print("Test failed: Task could not be deleted.")
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        if not any(t[0] == task_id for t in tasks):
            print("Test passed: Task is not present in the database.")
        else:
            print("Test failed: Task is still present in the database.")
        self.assertTrue(result)
        self.assertNotIn(task_id, [t[0] for t in tasks])

if __name__ == '__main__':
    unittest.main()