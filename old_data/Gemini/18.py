import unittest

class TodoItem:
    
    def __init__(self, title, description=""):
        self.title = title
        self.description = description
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def __str__(self):
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.title} - {self.description}"

class TodoManager:
    
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description=""):
        if not title:
            raise ValueError("Task title cannot be empty")
        new_item = TodoItem(title, description)
        self.tasks.append(new_item)
        return new_item

    def delete_task(self, index):
        try:
            return self.tasks.pop(index)
        except IndexError:
            return None

    def get_tasks(self):
        return self.tasks

class TestTodoApp(unittest.TestCase):
    
    def setUp(self):
        self.manager = TodoManager()

    def test_add_task(self):
        self.manager.add_task("Deploy to AWS", "Update Lambda functions")
        self.assertEqual(len(self.manager.get_tasks()), 1)
        self.assertEqual(self.manager.get_tasks()[0].title, "Deploy to AWS")

    def test_complete_task(self):
        task = self.manager.add_task("Code Review")
        task.mark_complete()
        self.assertTrue(self.manager.get_tasks()[0].completed)

    def test_delete_task(self):
        self.manager.add_task("Unit Testing")
        self.manager.delete_task(0)
        self.assertEqual(len(self.manager.get_tasks()), 0)

def run_cli():
    
    manager = TodoManager()
    
    
    manager.add_task("Inventory API", "Fix the bottleneck in the GET /items endpoint")
    manager.add_task("CloudFormation", "Review the new stack template for staging")
    
    print("--- John's Junior Dev Todo List ---")
    while True:
        print("\nCurrent Tasks:")
        for i, task in enumerate(manager.get_tasks()):
            print(f"{i}. {task}")
        
        print("\nOptions: [1] Add [2] Complete [3] Delete [4] Run Tests [5] Exit")
        choice = input("Select an option: ")

        if choice == '1':
            t = input("Enter title: ")
            d = input("Enter description: ")
            manager.add_task(t, d)
        elif choice == '2':
            idx = int(input("Enter task index to complete: "))
            tasks = manager.get_tasks()
            if 0 <= idx < len(tasks):
                tasks[idx].mark_complete()
        elif choice == '3':
            idx = int(input("Enter task index to delete: "))
            manager.delete_task(idx)
        elif choice == '4':
            print("\nRunning unit tests...")
            suite = unittest.TestLoader().loadTestsFromTestCase(TestTodoApp)
            unittest.TextTestRunner(verbosity=1).run(suite)
        elif choice == '5':
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    run_cli()