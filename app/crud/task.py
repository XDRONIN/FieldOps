from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def create_with_request_and_worker(
        self, db: Session, *, obj_in: TaskCreate
    ) -> Task:
        db_obj = Task(
            request_id=obj_in.request_id,
            worker_id=obj_in.worker_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_worker(
        self, db: Session, *, worker_id: int, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        return (
            db.query(self.model)
            .filter(Task.worker_id == worker_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_tasks_by_status_count(self, db: Session) -> dict:
        from sqlalchemy import func
        from app.models.task import TaskStatus
        return dict(db.query(Task.status, func.count(Task.id)).group_by(Task.status).all())

    def get_completed_tasks_count_by_worker(self, db: Session, *, worker_id: int) -> int:
        from app.models.task import TaskStatus
        return db.query(Task).filter(Task.worker_id == worker_id, Task.status == TaskStatus.COMPLETED).count()

task = CRUDTask(Task)
