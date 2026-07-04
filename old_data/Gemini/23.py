import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict
from abc import ABC, abstractmethod
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Task:
    
    def __init__(self, description: str):
        self.task_id = str(uuid.uuid4())
        self.description = description
        self.is_completed = False
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = self.created_at

    def complete(self) -> None:
        self.is_completed = True
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "description": self.description,
            "is_completed": self.is_completed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class TaskRepository(ABC):
    
    @abstractmethod
    def save(self, task: Task) -> None:
        pass

    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[Task]:
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

    def get_by_id(self, task_id: str) -> Optional[Task]:
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

    def add_task(self, description: str) -> str:
        if not description or len(description.strip()) == 0:
            raise ValueError("Task description cannot be empty")
        
        task = Task(description)
        self.repository.save(task)
        logger.info(f"Created task: {task.task_id}")
        return task.task_id

    def complete_task(self, task_id: str) -> bool:
        task = self.repository.get_by_id(task_id)
        if task:
            task.complete()
            self.repository.save(task)
            logger.info(f"Completed task: {task_id}")
            return True
        logger.warning(f"Task not found: {task_id}")
        return False

    def get_active_tasks(self) -> List[Task]:
        return [t for t in self.repository.list_all() if not t.is_completed]

    def get_all_tasks(self) -> List[Task]:
        return self.repository.list_all()

def main():
    
    
    repo = InMemoryTaskRepository()
    todo_service = TodoService(repo)

    try:
        
        task1_id = todo_service.add_task("Review Passkey implementation design")
        task2_id = todo_service.add_task("Finalize Remote Key provisioning protocols")
        
        print(f"Current Tasks: {[t.description for t in todo_service.get_active_tasks()]}")

        
        todo_service.complete_task(task1_id)

        
        active = todo_service.get_active_tasks()
        print(f"Remaining Tasks: {[t.description for t in active]}")
        
        
        all_tasks = todo_service.get_all_tasks()
        for t in all_tasks:
            status = "DONE" if t.is_completed else "PENDING"
            print(f"[{status}] {t.task_id}: {t.description}")

    except Exception as e:
        logger.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()