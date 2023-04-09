import unittest
from main import app

# Primary Author: Peyton Smith
# Current Semester: Spring 2023
# Unit Test 1 used to add a task
class TestAddTask(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_add_task(self):
        # Add our test task to the database
        response = self.app.post('/submit_task', data={
            'title': 'Test task',
            'description': 'This is a test task'
        })
        print(response.status_code)
        print(response.data)
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
