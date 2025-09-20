from pydantic import BaseModel

class UserStatusUpdate(BaseModel):
    is_active: bool

class WorkerApprovalUpdate(BaseModel):
    is_approved: bool
