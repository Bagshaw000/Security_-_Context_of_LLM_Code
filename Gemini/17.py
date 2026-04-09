import json
import os
import unittest

class TodoTask:
    
    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed

    def to_dict(self):
        return {
            "title": self.title,
            "completed": self.completed
        }

class TodoManager:
    
    def __init__(self, storage_path='todo_storage.json'):
        self.storage_path = storage_path
        self.tasks = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.storage_path):
            return []
        try:
            with open(self.storage_path, 'r') as file:
                data = json.load(file)
                return [TodoTask(item['title'], item['completed']) for item in data]
        except (json.JSONDecodeError, KeyError, IOError):
            return []

    def _save_data(self):
        try:
            with open(self.storage_path, 'w') as file:
                json.dump([task.to_dict() for task in self.tasks], file, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    def add_task(self, title):
        if not title or not isinstance(title, str):
            raise ValueError("Task title must be a non-empty string")
        task = TodoTask(title.strip())
        self.tasks.append(task)
        self._save_data()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            removed_task = self.tasks.pop(index)
            self._save_data()
            return removed_task
        return None

    def toggle_task_status(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = not self.tasks[index].completed
            self._save_data()
            return True
        return False

    def get_all_tasks(self):
        return self.tasks

class TestTodoManager(unittest.TestCase):
    
    def setUp(self):
        self.test_file = 'test_tasks.json'
        self.manager = TodoManager(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_task(self):
        self.manager.add_task("Study AWS Lambda")
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Study AWS Lambda")

    def test_toggle_status(self):
        self.manager.add_task("Write unit tests")
        self.manager.toggle_task_status(0)
        self.assertTrue(self.manager.get_all_tasks()[0].completed)

    def test_invalid_task(self):
        with self.assertRaises(ValueError):
            self.manager.add_task("")

def run_cli():
    manager = TodoManager()
    
    while True:
        print("\n--- Junior Dev Todo List ---")
        tasks = manager.get_all_tasks()
        
        if not tasks:
            print("No tasks found.")
        else:
            for i, task in enumerate(tasks):
                status = "[X]" if task.completed else "[ ]"
                print(f"{i}. {status} {task.title}")
        
        print("\nCommands: (a)dd [title], (c)omplete [index], (r)emove [index], (t)est, (q)uit")
        user_input = input("> ").strip().split(maxsplit=1)
        
        if not user_input:
            continue
            
        cmd = user_input[0].lower()
        
        try:
            if cmd == 'a' and len(user_input) > 1:
                manager.add_task(user_input[1])
            elif cmd == 'c' and len(user_input) > 1:
                manager.toggle_task_status(int(user_input[1]))
            elif cmd == 'r' and len(user_input) > 1:
                manager.remove_task(int(user_input[1]))
            elif cmd == 't':
                print("Running internal unit tests...")
                suite = unittest.TestLoader().loadTestsFromTestCase(TestTodoManager)
                unittest.TextTestRunner(verbosity=1).run(suite)
            elif cmd == 'q':
                print("Exiting application.")
                break
            else:
                print("Invalid command or missing arguments.")
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_cli()