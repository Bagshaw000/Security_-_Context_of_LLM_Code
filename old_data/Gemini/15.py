import json
import os
import unittest
from typing import List, Dict

class Task:
    
    def __init__(self, title: str, completed: bool = False):
        self.title = title
        self.completed = completed

    def to_dict(self) -> Dict:
        return {"title": self.title, "completed": self.completed}

    def __repr__(self):
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.title}"

class TodoManager:
    
    def __init__(self, storage_path: str = "tasks.json"):
        self.storage_path = storage_path
        self.tasks: List[Task] = self._load_from_disk()

    def _load_from_disk(self) -> List[Task]:
        if not os.path.exists(self.storage_path):
            return []
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                return [Task(**item) for item in data]
        except (json.JSONDecodeError, IOError):
            return []

    def _save_to_disk(self):
        with open(self.storage_path, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def add_task(self, title: str):
        if title:
            self.tasks.append(Task(title))
            self._save_to_disk()

    def mark_complete(self, index: int) -> bool:
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self._save_to_disk()
            return True
        return False

    def delete_task(self, index: int) -> bool:
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self._save_to_disk()
            return True
        return False

class TestTodoManager(unittest.TestCase):
    
    def setUp(self):
        self.test_file = "test_tasks.json"
        self.manager = TodoManager(self.test_file)
        self.manager.tasks = []

    def test_add_task(self):
        self.manager.add_task("Review AWS documentation")
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0].title, "Review AWS documentation")

    def test_mark_complete(self):
        self.manager.add_task("Deploy to staging")
        self.manager.mark_complete(0)
        self.assertTrue(self.manager.tasks[0].completed)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

def run_cli():
    manager = TodoManager()
    
    while True:
        print("\n--- Junior Dev Todo List ---")
        for i, task in enumerate(manager.tasks):
            print(f"{i}. {task}")
        
        print("\nOptions: [1] Add [2] Complete [3] Delete [4] Run Tests [5] Exit")
        choice = input("Select an option: ")

        if choice == '1':
            title = input("Enter task title: ")
            manager.add_task(title)
        elif choice == '2':
            idx = int(input("Enter task index to complete: "))
            manager.mark_complete(idx)
        elif choice == '3':
            idx = int(input("Enter task index to delete: "))
            manager.delete_task(idx)
        elif choice == '4':
            print("\nRunning unit tests...")
            suite = unittest.TestLoader().loadTestsFromTestCase(TestTodoManager)
            unittest.TextTestRunner(verbosity=1).run(suite)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    run_cli()