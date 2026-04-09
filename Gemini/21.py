import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict
from abc import ABC, abstractmethod

class TaskStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"

class Task:
    
    def __init__(self, title: str, description: str = "", priority: int = 1):
        self.task_id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def update_status(self, new_status: TaskStatus) -> None:
        self.status = new_status
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<Task(id={self.task_id[:8]}, title='{self.title}', status={self.status.value})>"

class ITodoRepository(ABC):
    
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

class InMemoryTodoRepository(ITodoRepository):
    
    def __init__(self):
        self._storage: Dict[str, Task] = {}

    def save(self, task: Task) -> None:
        self._storage[task.task_id] = task

    def find_by_id(self, task_id: str) -> Optional[Task]:
        return self._storage.get(task_id)

    def list_all(self) -> List[Task]:
        return list(self._storage.values())

    def delete(self, task_id: str) -> bool:
        if task_id in self._storage:
            del self._storage[task_id]
            return True
        return False

class TodoService:
    
    def __init__(self, repository: ITodoRepository):
        self._repository = repository

    def add_task(self, title: str, description: str = "") -> str:
        if not title.strip():
            raise ValueError("Task title is required for registration.")
        
        task = Task(title, description)
        self._repository.save(task)
        return task.task_id

    def complete_task(self, task_id: str) -> None:
        task = self._repository.find_by_id(task_id)
        if not task:
            raise LookupError(f"Task with ID {task_id} not found in the registry.")
        
        task.update_status(TaskStatus.COMPLETED)
        self._repository.save(task)

    def get_active_tasks(self) -> List[Task]:
        all_tasks = self._repository.list_all()
        return [t for t in all_tasks if t.status != TaskStatus.COMPLETED]

    def get_task_summary(self) -> str:
        tasks = self._repository.list_all()
        completed = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
        pending = len(tasks) - completed
        return f"Total Tasks: {len(tasks)} | Pending: {pending} | Completed: {completed}"

def main():
    
    
    repository = InMemoryTodoRepository()
    todo_manager = TodoService(repository)

    
    print("Initializing Todo Service...")
    
    
    id1 = todo_manager.add_task(
        "Implement Passkey Provisioning", 
        "Design the handshake protocol for hardware-backed security keys."
    )
    
    
    id2 = todo_manager.add_task(
        "Update Account-Linking Service", 
        "Migrate legacy OAuth flow to OIDC-compliant identity provider."
    )

    print(f"Created Task 1: {id1}")
    print(f"Created Task 2: {id2}")

    print("\n--- Current Active Tasks ---")
    for task in todo_manager.get_active_tasks():
        print(f"[{task.status.value}] {task.title}: {task.description}")

    
    print(f"\nProcessing Task: {id1}...")
    todo_manager.complete_task(id1)

    print("\n--- Updated Summary ---")
    print(todo_manager.get_task_summary())

    print("\nRemaining Work Items:")
    for task in todo_manager.get_active_tasks():
        print(f"-> {task.title}")

if __name__ == "__main__":
    main()