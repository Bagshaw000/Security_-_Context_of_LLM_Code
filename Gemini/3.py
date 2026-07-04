import json
import os
import unittest

class TodoItem:
    
    def __init__(self, task_id, title, completed=False):
        self.task_id = task_id
        self.title = title
        self.completed = completed

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "completed": self.completed
        }

class TodoManager:
    
    def __init__(self, storage_file='todos.json'):
        self.storage_file = storage_file
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    return [TodoItem(t['id'], t['title'], t['completed']) for t in data]
            except (json.JSONDecodeError, KeyError, IOError):
                return []
        return []

    def _save_tasks(self):
        
        try:
            with open(self.storage_file, 'w') as f:
                json.dump([t.to_dict() for t in self.tasks], f, indent=4)
        except IOError as e:
            print(f"Error saving tasks: {e}")

    def add_task(self, title):
        if not title.strip():
            return None
        new_id = max([t.task_id for t in self.tasks], default=0) + 1
        new_task = TodoItem(new_id, title)
        self.tasks.append(new_task)
        self._save_tasks()
        return new_task

    def delete_task(self, task_id):
        initial_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        if len(self.tasks) != initial_count:
            self._save_tasks()
            return True
        return False

    def toggle_task(self, task_id):
        for t in self.tasks:
            if t.task_id == task_id:
                t.completed = not t.completed
                self._save_tasks()
                return True
        return False

    def get_all_tasks(self):
        return self.tasks

def run_cli():
    
    manager = TodoManager()
    
    while True:
        print("\n--- TODO LIST MANAGER ---")
        tasks = manager.get_all_tasks()
        if not tasks:
            print("No tasks found.")
        else:
            for t in tasks:
                status = "[X]" if t.completed else "[ ]"
                print(f"{t.task_id}. {status} {t.title}")
        
        print("\nOptions: (a)dd, (d)elete, (t)oggle, (q)uit")
        choice = input("> ").lower().strip()

        if choice == 'a':
            title = input("Enter task title: ")
            manager.add_task(title)
        elif choice == 'd':
            try:
                tid = int(input("Enter task ID to delete: "))
                if not manager.delete_task(tid):
                    print("Task ID not found.")
            except ValueError:
                print("Invalid input. Please enter a numerical ID.")
        elif choice == 't':
            try:
                tid = int(input("Enter task ID to toggle: "))
                if not manager.toggle_task(tid):
                    print("Task ID not found.")
            except ValueError:
                print("Invalid input. Please enter a numerical ID.")
        elif choice == 'q':
            print("Exiting application...")
            break
        else:
            print("Invalid option.")

class TestTodoApp(unittest.TestCase):
    
    def setUp(self):
        self.test_file = 'test_todos.json'
        self.manager = TodoManager(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_task(self):
        task = self.manager.add_task("Unit Test Task")
        self.assertIsNotNone(task)
        self.assertEqual(len(self.manager.get_all_tasks()), 1)
        self.assertEqual(self.manager.get_all_tasks()[0].title, "Unit Test Task")

    def test_toggle_task(self):
        task = self.manager.add_task("Toggle Me")
        self.assertFalse(task.completed)
        self.manager.toggle_task(task.task_id)
        self.assertTrue(self.manager.get_all_tasks()[0].completed)

    def test_delete_task(self):
        task = self.manager.add_task("Delete Me")
        self.manager.delete_task(task.task_id)
        self.assertEqual(len(self.manager.get_all_tasks()), 0)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        sys.argv = sys.argv[:1]
        unittest.main()
    else:
        run_cli()