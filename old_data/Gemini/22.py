import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional, Dict
from abc import ABC, abstractmethod

class TaskStatus(Enum):
    PENDING = auto()
    COMPLETED = auto()
    ARCHIVED = auto()

@dataclass
class Task:
    
    description: str
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def mark_complete(self):
        self.status = TaskStatus.COMPLETED
        self.updated_at = datetime.utcnow()

class TaskRepository(ABC):
    
    @abstractmethod
    def save(self, task: Task) -> None:
        pass

    @abstractmethod
    def find_by_id(self, task_id: str) -> Optional[Task]:
        pass

    @abstractmethod
    def list_all(self) -> List[Task]:
        pass

    @abstractmethod
    def delete(self, task_id: str) -> bool:
        pass

class InMemoryTaskRepository(TaskRepository):
    
    def __init__(self):
        self._storage: Dict[str, Task] = {}

    def save(self, task: Task) -> None:
        self._storage[task.task_id] = task

    def find_by_id(self, task_id: str) -> Optional[Task]:
        return self._storage.get(task_id)

    def list_all(self) -> List[Task]:
        return sorted(list(self._storage.values()), key=lambda x: x.created_at)

    def delete(self, task_id: str) -> bool:
        if task_id in self._storage:
            del self._storage[task_id]
            return True
        return False

class TodoService:
    
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def add_todo(self, description: str) -> Task:
        if not description or len(description.strip()) == 0:
            raise ValueError("Task description cannot be empty.")
        
        task = Task(description=description.strip())
        self.repository.save(task)
        return task

    def complete_todo(self, task_id: str) -> None:
        task = self.repository.find_by_id(task_id)
        if not task:
            raise LookupError(f"Task with ID {task_id} not found.")
        task.mark_complete()
        self.repository.save(task)

    def get_all_todos(self) -> List[Task]:
        return self.repository.list_all()

    def remove_todo(self, task_id: str) -> bool:
        return self.repository.delete(task_id)

def main():
    
    
    repository = InMemoryTaskRepository()
    todo_service = TodoService(repository)

    print("--- Amazon Device Management Todo System ---")
    
    
    task1 = todo_service.add_todo("Implement Remote Key Provisioning logic")
    task2 = todo_service.add_todo("Audit Passkey authentication flow")
    
    print(f"Added Task: {task1.description} (ID: {task1.task_id})")
    print(f"Added Task: {task2.description} (ID: {task2.task_id})")

    todo_service.complete_todo(task1.task_id)
    print(f"\nUpdated Task Status: {task1.description} is now {task1.status.name}")

    print("\nCurrent Todo List:")
    for task in todo_service.get_all_todos():
        status_icon = "[x]" if task.status == TaskStatus.COMPLETED else "[ ]"
        print(f"{status_icon} {task.description} (Created: {task.created_at.strftime('%Y-%m-%d %H:%M')})")

if __name__ == "__main__":
    main()