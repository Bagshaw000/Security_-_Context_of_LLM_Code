import json
import uuid
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from enum import Enum
from typing import List, Dict, Optional


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

@dataclass
class Task:
    
    id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING

    def to_dict(self) -> Dict:
        data = asdict(self)
        data['status'] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            status=TaskStatus(data['status'])
        )

class StorageProvider(ABC):
    
    @abstractmethod
    def save(self, tasks: List[Task]) -> None:
        pass

    @abstractmethod
    def load(self) -> List[Task]:
        pass

class FileStorageProvider(StorageProvider):
    
    def __init__(self, file_path: str = "tasks_store.json"):
        self.file_path = file_path

    def save(self, tasks: List[Task]) -> None:
        try:
            with open(self.file_path, 'w') as f:
                json.dump([t.to_dict() for t in tasks], f, indent=4)
        except IOError as e:
            logger.error(f"Failed to persist data to {self.file_path}: {e}")

    def load(self) -> List[Task]:
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

class TodoManager:
    
    def __init__(self, storage: StorageProvider):
        self._storage = storage
        self._tasks: Dict[str, Task] = {t.id: t for t in self._storage.load()}

    def create_task(self, title: str, description: str = "") -> str:
        if not title:
            raise ValueError("Task title cannot be empty.")
        
        task_id = str(uuid.uuid4())[:8]  
        new_task = Task(id=task_id, title=title, description=description)
        self._tasks[task_id] = new_task
        self._sync_storage()
        logger.info(f"Task created: {task_id}")
        return task_id

    def list_tasks(self, include_completed: bool = True) -> List[Task]:
        tasks = list(self._tasks.values())
        if not include_completed:
            return [t for t in tasks if t.status == TaskStatus.PENDING]
        return tasks

    def mark_completed(self, task_id: str) -> bool:
        if task_id in self._tasks:
            self._tasks[task_id].status = TaskStatus.COMPLETED
            self._sync_storage()
            return True
        return False

    def delete_task(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            self._sync_storage()
            return True
        return False

    def _sync_storage(self) -> None:
        self._storage.save(list(self._tasks.values()))

class TodoCLI:
    
    def __init__(self, manager: TodoManager):
        self.manager = manager

    def run(self):
        actions = {
            "1": self._ui_add,
            "2": self._ui_list,
            "3": self._ui_complete,
            "4": self._ui_delete,
            "5": exit
        }

        while True:
            print("\n--- Task Management System ---")
            print("1. Add Task\n2. List Tasks\n3. Complete Task\n4. Delete Task\n5. Exit")
            choice = input("Select option: ").strip()
            
            action = actions.get(choice)
            if action:
                try:
                    action()
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Invalid selection.")

    def _ui_add(self):
        title = input("Enter title: ")
        desc = input("Enter description: ")
        tid = self.manager.create_task(title, desc)
        print(f"Created Task ID: {tid}")

    def _ui_list(self):
        tasks = self.manager.list_tasks()
        if not tasks:
            print("No tasks found.")
            return
        for t in tasks:
            check = "[X]" if t.status == TaskStatus.COMPLETED else "[ ]"
            print(f"{check} {t.id} | {t.title}: {t.description}")

    def _ui_complete(self):
        tid = input("Enter Task ID to complete: ")
        if self.manager.mark_completed(tid):
            print("Success.")
        else:
            print("ID not found.")

    def _ui_delete(self):
        tid = input("Enter Task ID to delete: ")
        if self.manager.delete_task(tid):
            print("Deleted.")
        else:
            print("ID not found.")

if __name__ == "__main__":
    
    storage = FileStorageProvider()
    service = TodoManager(storage)
    app = TodoCLI(service)
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nShutting down gracefully.")