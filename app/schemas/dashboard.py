from pydantic import BaseModel
from typing import Dict, Any

class AdminDashboard(BaseModel):
    total_users: int
    total_workers: int
    pending_approvals: int
    tasks_by_status: Dict[str, int]
    avg_rating: float | None

class WorkerDashboard(BaseModel):
    assigned_tasks: int
    completed_tasks: int
    performance_stats: Dict[str, Any] # e.g., avg_completion_time, avg_rating

class UserDashboard(BaseModel):
    requests_created: int
    requests_by_status: Dict[str, int]
    avg_rating_given: float | None
