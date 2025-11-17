import unittest
from todo import app, db, Todo

class TodoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'To-Do List', response.data)

    def test_add_task(self):
        response = self.client.post('/add', data={'content': 'Test Task'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Task', response.data)

    def test_complete_task(self):
        with self.app.app_context():
            task = Todo(content='Incomplete Task')
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        response = self.client.get(f'/complete/{task_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Incomplete Task', response.data)  # Because it's moved to complete

    def test_delete_task(self):
        with self.app.app_context():
            task = Todo(content='Task to Delete')
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        response = self.client.get(f'/delete/{task_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Task to Delete', response.data)

if __name__ == '__main__':
    unittest.main()
