from pydantic import BaseModel
from app.models.task import TaskStatus

# Shared properties
class TaskBase(BaseModel):
    status: TaskStatus | None = None
    proof_notes: str | None = None
    proof_photos: str | None = None

# Properties to receive on creation
class TaskCreate(BaseModel):
    request_id: int
    worker_id: int

# Properties to receive on update
class TaskUpdate(TaskBase):
    pass

class TaskStatusUpdate(BaseModel):
    status: TaskStatus

from pydantic import ConfigDict    

# Properties shared by models stored in DB
class TaskInDBBase(TaskBase):
    id: int
    request_id: int
    worker_id: int

    model_config = ConfigDict(from_attributes=True)

# Properties to return to client
class Task(TaskInDBBase):
    pass

# Properties stored in DB
class TaskInDB(TaskInDBBase):
    pass
