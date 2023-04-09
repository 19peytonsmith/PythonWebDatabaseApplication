import unittest
from app import app, getLastRow

# Primary Author: Peyton Smith
# Current Semester: Spring 2023
# Unit Test 2 used to add a task and then delete it after
class TestDeleteTask(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        # Add our test task to the database
        response = self.app.post('/submit_task', data={
            'title': 'To be deleted task',
            'description': 'This is a to be deleted task'
        })
        print(response.status_code)
        print(response.data)
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        self.app_context.pop()

    def test_delete_task(self):
        # Get the ID of the test task from the database
        with app.app_context():
            lastID = getLastRow()

        # Send a POST request to the delete_task endpoint with the last row's ID (the one we just added)
        response = self.app.post(f'/delete_task/{lastID}')
        self.assertEqual(response.status_code, 302)

        # Check that the task was deleted from the database
        with app.app_context():
            lastIDUpdated = getLastRow()
            self.assertNotEqual(lastID, lastIDUpdated)

if __name__ == '__main__':
    unittest.main()
