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
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 0, "Should return an empty list when there are no tasks.")
        self.assertListEqual(tasks, [], "Should return an empty list when there are no tasks.")

    def test_show_one_incomplete_task(self):
        desc = "Single task"
        task_id = add_task_db(desc, db_name=self.TEST_DB_NAME)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1, "There should be one item in the list when there is one task.")
        
        expected_task = (task_id, desc, 0)
        self.assertEqual(tasks[0], expected_task, "Task information should be correct.")

    def test_show_multiple_tasks_mixed_status(self):
        desc1 = "First task (incomplete)"
        id1 = add_task_db(desc1, db_name=self.TEST_DB_NAME)

        desc2 = "Second task (completed)"
        id2 = add_task_db(desc2, db_name=self.TEST_DB_NAME)
        complete_task_db(id2, db_name=self.TEST_DB_NAME)

        desc3 = "Third task (incomplete)"
        id3 = add_task_db(desc3, db_name=self.TEST_DB_NAME)

        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 3, "There should be three tasks in the list.")

        expected_tasks_data = [
            (id1, desc1, 0),
            (id2, desc2, 1),
            (id3, desc3, 0)
        ]
  
        actual_tasks_data = [(task[0], task[1], task[2]) for task in tasks]
        
        self.assertListEqual(actual_tasks_data, expected_tasks_data, "Task list and statuses should be correct.")

    def test_show_one_completed_task(self):
        desc = "Completed task"
        task_id = add_task_db(desc, db_name=self.TEST_DB_NAME)
        complete_task_db(task_id, db_name=self.TEST_DB_NAME)

        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1, "There should be one item in the list when there is one task.")

        expected_task = (task_id, desc, 1)
        self.assertEqual(tasks[0], expected_task, "Completed task information should be correct.")

    def test_show_tasks_ordered_by_id(self):
        task1_id = add_task_db("First task", db_name=self.TEST_DB_NAME)
        task2_id = add_task_db("Second task", db_name=self.TEST_DB_NAME)
        task3_id = add_task_db("Third task", db_name=self.TEST_DB_NAME)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 3)
        
        self.assertEqual(tasks[0][0], task1_id)
        self.assertEqual(tasks[1][0], task2_id)
        self.assertEqual(tasks[2][0], task3_id)

    def test_show_tasks_with_special_characters(self):
        special_desc = "Task with !@#$%^&*()_+-=[]{}|;':\",./<>?"
        task_id = add_task_db(special_desc, db_name=self.TEST_DB_NAME)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][1], special_desc)

    def test_show_tasks_with_unicode(self):
        unicode_desc = "Task with émojis 🎉 and ñ characters"
        task_id = add_task_db(unicode_desc, db_name=self.TEST_DB_NAME)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][1], unicode_desc)

    def test_show_tasks_with_newlines(self):
        multiline_desc = "Line 1\nLine 2\nLine 3"
        task_id = add_task_db(multiline_desc, db_name=self.TEST_DB_NAME)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][1], multiline_desc)

    def test_show_tasks_with_very_long_description(self):
        long_desc = "A" * 10000
        task_id = add_task_db(long_desc, db_name=self.TEST_DB_NAME)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][1], long_desc)

    def test_show_tasks_after_completion(self):
        task_id = add_task_db("Original task", db_name=self.TEST_DB_NAME)
        
        tasks_before = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(tasks_before[0][2], 0)
        
        complete_task_db(task_id, db_name=self.TEST_DB_NAME)
        
        tasks_after = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(tasks_after[0][2], 1)

    def test_show_tasks_after_deletion(self):
        from database import delete_task_db
        
        task1_id = add_task_db("Task 1", db_name=self.TEST_DB_NAME)
        task2_id = add_task_db("Task 2", db_name=self.TEST_DB_NAME)
        
        tasks_before = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks_before), 2)
        
        delete_task_db(task1_id, db_name=self.TEST_DB_NAME)
        
        tasks_after = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks_after), 1)
        self.assertEqual(tasks_after[0][0], task2_id)

    def test_show_tasks_with_numeric_description(self):
        numeric_desc = "12345"
        task_id = add_task_db(numeric_desc, db_name=self.TEST_DB_NAME)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][1], numeric_desc)

    def test_show_tasks_with_empty_string_description(self):
        empty_desc = ""
        task_id = add_task_db(empty_desc, db_name=self.TEST_DB_NAME)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][1], empty_desc)

    def test_show_tasks_with_whitespace_description(self):
        whitespace_desc = "   "
        task_id = add_task_db(whitespace_desc, db_name=self.TEST_DB_NAME)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][1], whitespace_desc)

    def test_show_tasks_after_clear_and_recreate(self):
        task1_id = add_task_db("Original task", db_name=self.TEST_DB_NAME)
        tasks_before = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks_before), 1)
        
        clear_tasks_table(db_name=self.TEST_DB_NAME)
        tasks_after_clear = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks_after_clear), 0)
        
        task2_id = add_task_db("New task", db_name=self.TEST_DB_NAME)
        tasks_after_recreate = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks_after_recreate), 1)
        self.assertEqual(tasks_after_recreate[0][0], task2_id)

    def test_show_tasks_data_structure(self):
        task_id = add_task_db("Test task", db_name=self.TEST_DB_NAME)
        
        tasks = get_tasks_db(db_name=self.TEST_DB_NAME)
        self.assertEqual(len(tasks), 1)
        
        task = tasks[0]
        self.assertEqual(len(task), 3)
        self.assertIsInstance(task[0], int)
        self.assertIsInstance(task[1], str)
        self.assertIsInstance(task[2], int)

    def test_show_tasks_with_print(self):
        print("Testing show_tasks() function.")
        print("Database connection is initialized.")
        clear_tasks_table(db_name=self.TEST_DB_NAME)
        print("Adding two tasks to the database.")
        desc1 = "Task 1 for show"
        desc2 = "Task 2 for show"
        add_task_db(desc1, db_name=self.TEST_DB_NAME)
        add_task_db(desc2, db_name=self.TEST_DB_NAME)
        print("Retrieving tasks from the database.")
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