import json
import os
import unittest

class TodoManager:
    
    def __init__(self, file_path='tasks.json'):
        self.file_path = file_path
        self.tasks = self._load_from_disk()

    def _load_from_disk(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError):
                return []
        return []

    def _save_to_disk(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.tasks, f, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    def add_task(self, description):
        task_id = max([t['id'] for t in self.tasks], default=0) + 1
        new_task = {
            'id': task_id,
            'description': description,
            'status': 'pending'
        }
        self.tasks.append(new_task)
        self._save_to_disk()
        return task_id

    def list_tasks(self, include_completed=True):
        if include_completed:
            return self.tasks
        return [t for t in self.tasks if t['status'] == 'pending']

    def complete_task(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = 'completed'
                self._save_to_disk()
                return True
        return False

    def delete_task(self, task_id):
        initial_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        if len(self.tasks) < initial_len:
            self._save_to_disk()
            return True
        return False

class TestTodoManager(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test_tasks.json'
        self.manager = TodoManager(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_task(self):
        tid = self.manager.add_task("Review PR for inventory tool")
        self.assertEqual(len(self.manager.list_tasks()), 1)
        self.assertEqual(self.manager.list_tasks()[0]['id'], tid)

    def test_complete_task(self):
        tid = self.manager.add_task("Deploy to AWS staging")
        self.manager.complete_task(tid)
        tasks = self.manager.list_tasks()
        self.assertEqual(tasks[0]['status'], 'completed')

    def test_delete_task(self):
        tid = self.manager.add_task("Write unit tests")
        self.manager.delete_task(tid)
        self.assertEqual(len(self.manager.list_tasks()), 0)

def main():
    manager = TodoManager()
    
    while True:
        print("\n--- TODO APPLICATION ---")
        tasks = manager.list_tasks()
        if not tasks:
            print("No tasks found.")
        for t in tasks:
            mark = "[X]" if t['status'] == 'completed' else "[ ]"
            print(f"{t['id']}. {mark} {t['description']}")
        
        print("\nMenu: [1] Add [2] Complete [3] Delete [4] Run Tests [5] Exit")
        choice = input("Select an option: ")

        if choice == '1':
            desc = input("Task description: ")
            manager.add_task(desc)
        elif choice == '2':
            try:
                tid = int(input("Enter Task ID to complete: "))
                if not manager.complete_task(tid):
                    print("Task ID not found.")
            except ValueError:
                print("Please enter a valid numeric ID.")
        elif choice == '3':
            try:
                tid = int(input("Enter Task ID to delete: "))
                if not manager.delete_task(tid):
                    print("Task ID not found.")
            except ValueError:
                print("Please enter a valid numeric ID.")
        elif choice == '4':
            print("\nRunning Suite...")
            suite = unittest.TestLoader().loadTestsFromTestCase(TestTodoManager)
            unittest.TextTestRunner(verbosity=1).run(suite)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()