import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import init_db, add_task_db, get_tasks_db, clear_tasks_table

class TestAddTask(unittest.TestCase):
    TEST_DB_NAME = "test_add_tasks.db"

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

    def test_add_single_task(self):
        description = "First test task"
        task_id = add_task_db(description, db_name=self.TEST_DB_NAME)
        self.assertIsNotNone(task_id, "Task ID should not be None.")
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1, "There should be one task in the database.")
        self.assertEqual(tasks[0][1], description, "Task description should match.")
        self.assertEqual(tasks[0][2], 0, "Task should be incomplete.")

    def test_add_multiple_tasks(self):
        add_task_db("Task 1", db_name=self.TEST_DB_NAME)
        add_task_db("Task 2", db_name=self.TEST_DB_NAME)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 2, "There should be two tasks in the database.")

    def test_add_empty_description(self):
        task_id = add_task_db("", db_name=self.TEST_DB_NAME)
        self.assertIsNotNone(task_id)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(tasks[0][1], "")

    def test_add_whitespace_only_description(self):
        task_id = add_task_db("   ", db_name=self.TEST_DB_NAME)
        self.assertIsNotNone(task_id)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(tasks[0][1], "   ")

    def test_add_very_long_description(self):
        long_description = "A" * 10000
        task_id = add_task_db(long_description, db_name=self.TEST_DB_NAME)
        self.assertIsNotNone(task_id)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(tasks[0][1], long_description)

    def test_add_special_characters(self):
        special_desc = "Task!@#$%^&*()_+-=[]{}|;':\",./<>?"
        task_id = add_task_db(special_desc, db_name=self.TEST_DB_NAME)
        self.assertIsNotNone(task_id)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(tasks[0][1], special_desc)

    def test_add_unicode_characters(self):
        unicode_desc = "Task with émojis 🎉 and ñ characters"
        task_id = add_task_db(unicode_desc, db_name=self.TEST_DB_NAME)
        self.assertIsNotNone(task_id)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(tasks[0][1], unicode_desc)

    def test_add_numeric_description(self):
        numeric_desc = "12345"
        task_id = add_task_db(numeric_desc, db_name=self.TEST_DB_NAME)
        self.assertIsNotNone(task_id)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(tasks[0][1], numeric_desc)

    def test_add_sql_injection_attempt(self):
        sql_injection = "'; DROP TABLE tasks; --"
        task_id = add_task_db(sql_injection, db_name=self.TEST_DB_NAME)
        self.assertIsNotNone(task_id)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][1], sql_injection)

    def test_add_multiple_tasks_sequential_ids(self):
        task1_id = add_task_db("Task 1", db_name=self.TEST_DB_NAME)
        task2_id = add_task_db("Task 2", db_name=self.TEST_DB_NAME)
        task3_id = add_task_db("Task 3", db_name=self.TEST_DB_NAME)
        
        self.assertEqual(task1_id, 1)
        self.assertEqual(task2_id, 2)
        self.assertEqual(task3_id, 3)

    def test_add_task_with_newlines(self):
        multiline_desc = "Line 1\nLine 2\nLine 3"
        task_id = add_task_db(multiline_desc, db_name=self.TEST_DB_NAME)
        self.assertIsNotNone(task_id)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(tasks[0][1], multiline_desc)

    def test_add_and_show_tasks_with_print(self):
        print("Testing get_all_tasks() function.")
        print("Database connection is initialized.")
        clear_tasks_table(db_name=self.TEST_DB_NAME)
        print("Checking if there are any tasks in the database before the test starts.")
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        if not tasks:
            print("Test setup passed: No tasks found in the database before the test started.")
        else:
            print("Test setup failed: There are tasks in the database before the test started.")
        print("Adding two tasks to the database.")
        desc1 = "Task 1"
        desc2 = "Task 2"
        add_task_db(desc1, db_name=self.TEST_DB_NAME)
        add_task_db(desc2, db_name=self.TEST_DB_NAME)
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        if len(tasks) == 2:
            print("Test passed: Expected 2 tasks and correct number of tasks retrieved.")
        else:
            print("Test failed: Task count mismatch.")
        descriptions = [task[1] for task in tasks]
        if desc1 in descriptions and desc2 in descriptions:
            print("Test passed: Task descriptions match correctly.")
        else:
            print("Test failed: Task descriptions do not match.")
        self.assertEqual(len(tasks), 2)
        self.assertIn(desc1, descriptions)
        self.assertIn(desc2, descriptions)

if __name__ == '__main__':
    unittest.main()