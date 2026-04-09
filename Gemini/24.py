import json
import uuid
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"

@dataclass
class Task:
    title: str
    description: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        data = asdict(self)
        data['status'] = self.status.value
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            status=TaskStatus(data['status']),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at'])
        )

class StorageProvider(ABC):
    @abstractmethod
    def save(self, tasks: List[Task]) -> None:
        pass

    @abstractmethod
    def load(self) -> List[Task]:
        pass

class FileStorageProvider(StorageProvider):
    def __init__(self, filename: str = "todo_store.json"):
        self.filename = filename

    def save(self, tasks: List[Task]) -> None:
        try:
            with open(self.filename, 'w') as f:
                json.dump([task.to_dict() for task in tasks], f, indent=4)
        except IOError as e:
            logging.error(f"Failed to write to storage: {e}")

    def load(self) -> List[Task]:
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

class TodoService:
    
    def __init__(self, storage: StorageProvider):
        self._storage = storage
        self._tasks: Dict[str, Task] = {t.id: t for t in self._storage.load()}

    def add_task(self, title: str, description: str) -> str:
        task = Task(title=title, description=description)
        self._tasks[task.id] = task
        self._persist()
        logging.info(f"Task created: {task.id}")
        return task.id

    def get_all_tasks(self, include_archived: bool = False) -> List[Task]:
        tasks = list(self._tasks.values())
        if not include_archived:
            return [t for t in tasks if t.status != TaskStatus.ARCHIVED]
        return tasks

    def update_status(self, task_id: str, status: TaskStatus) -> bool:
        if task_id not in self._tasks:
            logging.warning(f"Attempted to update non-existent task: {task_id}")
            return False
        
        task = self._tasks[task_id]
        task.status = status
        task.updated_at = datetime.now()
        self._persist()
        return True

    def delete_task(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            self._persist()
            return True
        return False

    def _persist(self) -> None:
        self._storage.save(list(self._tasks.values()))

class TodoCLI:
    def __init__(self, service: TodoService):
        self.service = service

    def run(self):
        print("--- Amazon Device Systems: Internal Task Tracker ---")
        while True:
            print("\n1. Add Task\n2. List Tasks\n3. Complete Task\n4. Delete Task\n5. Exit")
            choice = input("Select an option: ")

            if choice == '1':
                t = input("Title: ")
                d = input("Description: ")
                self.service.add_task(t, d)
            elif choice == '2':
                tasks = self.service.get_all_tasks()
                for t in tasks:
                    print(f"[{t.id[:8]}] {t.title} - {t.status.value}")
            elif choice == '3':
                tid = input("Enter Task ID prefix: ")
                
                target = next((t.id for t in self.service.get_all_tasks() if t.id.startswith(tid)), None)
                if target:
                    self.service.update_status(target, TaskStatus.COMPLETED)
                else:
                    print("Task not found.")
            elif choice == '4':
                tid = input("Enter Task ID prefix: ")
                target = next((t.id for t in self.service.get_all_tasks() if t.id.startswith(tid)), None)
                if target:
                    self.service.delete_task(target)
            elif choice == '5':
                break
            else:
                print("Invalid selection.")

if __name__ == "__main__":
    
    storage = FileStorageProvider()
    todo_service = TodoService(storage)
    app = TodoCLI(todo_service)
    app.run()