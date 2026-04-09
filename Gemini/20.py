import uuid
from datetime import datetime, timezone
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
        self.status = TaskStatus.PENDING
        self.priority = priority
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = self.created_at

    def update_status(self, new_status: TaskStatus):
        self.status = new_status
        self.updated_at = datetime.now(timezone.utc)

    def __repr__(self):
        return f"<Task(id={self.task_id}, title='{self.title}', status={self.status.value})>"

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
        return list(self._storage.values())

    def delete(self, task_id: str) -> bool:
        if task_id in self._storage:
            del self._storage[task_id]
            return True
        return False

class TodoService:
    
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, title: str, description: str = "", priority: int = 1) -> str:
        if not title.strip():
            raise ValueError("Task title cannot be empty.")
        
        new_task = Task(title, description, priority)
        self.repository.save(new_task)
        return new_task.task_id

    def mark_task_complete(self, task_id: str) -> None:
        task = self.repository.find_by_id(task_id)
        if not task:
            raise LookupError(f"Task with ID {task_id} not found.")
        
        task.update_status(TaskStatus.COMPLETED)
        self.repository.save(task)

    def get_pending_tasks(self) -> List[Task]:
        return [t for t in self.repository.list_all() if t.status != TaskStatus.COMPLETED]

    def remove_task(self, task_id: str) -> bool:
        return self.repository.delete(task_id)

def main():
    
    
    repository = InMemoryTaskRepository()
    todo_service = TodoService(repository)

    
    try:
        
        task_1_id = todo_service.create_task(
            "Finalize Passkey Integration", 
            "Implement WebAuthn credentials for device registration."
        )
        
        
        task_2_id = todo_service.create_task(
            "Review Remote Key Provisioning Design",
            "Evaluate latency impacts on the device-authentication fleet.",
            priority=5
        )

        print(f"Service initialized. Active Tasks: {len(todo_service.get_pending_tasks())}")

        
        todo_service.mark_task_complete(task_1_id)
        print(f"Task {task_1_id} marked as complete.")

        
        remaining = todo_service.get_pending_tasks()
        for task in remaining:
            print(f"Pending: {task.title} (Priority: {task.priority})")

    except Exception as e:
        print(f"Application Error: {str(e)}")

if __name__ == "__main__":
    main()