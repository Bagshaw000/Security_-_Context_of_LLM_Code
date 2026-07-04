import uuid
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Task:
    
    description: str
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    completed: bool = False

    def __str__(self) -> str:
        status = "[X]" if self.completed else "[ ]"
        return f"{status} {self.task_id}: {self.description}"

class TodoList:
    
    def __init__(self):
        self._tasks: List[Task] = []

    def add_task(self, description: str) -> str:
        if not description:
            raise ValueError("Task description cannot be empty.")
        new_task = Task(description=description)
        self._tasks.append(new_task)
        return new_task.task_id

    def remove_task(self, task_id: str) -> bool:
        initial_count = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.task_id != task_id]
        return len(self._tasks) < initial_count

    def complete_task(self, task_id: str) -> bool:
        for task in self._tasks:
            if task.task_id == task_id:
                task.completed = True
                return True
        return False

    def get_all_tasks(self) -> List[Task]:
        return self._tasks

def cli_interface():
    
    manager = TodoList()
    print("Bristol Inventory-style Todo Manager")
    print("Commands: add <desc>, list, complete <id>, remove <id>, quit")

    while True:
        try:
            user_input = input("\n> ").strip().split(" ", 1)
            cmd = user_input[0].lower()
            args = user_input[1] if len(user_input) > 1 else None

            if cmd == "quit":
                break
            elif cmd == "add" and args:
                tid = manager.add_task(args)
                print(f"Task created with ID: {tid}")
            elif cmd == "list":
                tasks = manager.get_all_tasks()
                if not tasks:
                    print("List is currently empty.")
                for t in tasks:
                    print(t)
            elif cmd == "complete" and args:
                success = manager.complete_task(args)
                print("Task updated." if success else "Task ID not found.")
            elif cmd == "remove" and args:
                success = manager.remove_task(args)
                print("Task removed." if success else "Task ID not found.")
            else:
                print("Unknown command or missing arguments.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    
    
    cli_interface()