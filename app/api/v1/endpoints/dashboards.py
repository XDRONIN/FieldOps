from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/admin", response_model=schemas.AdminDashboard)
def get_admin_dashboard(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Retrieve admin dashboard data.
    """
    total_users = crud.user.get_users_count(db)
    total_workers = crud.user.get_workers_count(db)
    pending_approvals = crud.user.get_pending_approvals_count(db)
    tasks_by_status = crud.task.get_tasks_by_status_count(db)
    avg_rating = crud.rating.get_average_rating(db)

    return {
        "total_users": total_users,
        "total_workers": total_workers,
        "pending_approvals": pending_approvals,
        "tasks_by_status": tasks_by_status,
        "avg_rating": avg_rating,
    }

@router.get("/worker", response_model=schemas.WorkerDashboard)
def get_worker_dashboard(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_worker),
) -> Any:
    """
    Retrieve worker dashboard data.
    """
    assigned_tasks = len(crud.task.get_multi_by_worker(db, worker_id=current_user.id))
    completed_tasks = crud.task.get_completed_tasks_count_by_worker(db, worker_id=current_user.id)

    return {
        "assigned_tasks": assigned_tasks,
        "completed_tasks": completed_tasks,
        "performance_stats": {},
    }

@router.get("/user", response_model=schemas.UserDashboard)
def get_user_dashboard(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve user dashboard data.
    """
    requests_created = len(crud.service_request.get_multi_by_owner(db, user_id=current_user.id))
    requests_by_status = crud.service_request.get_requests_by_status_count_by_owner(db, user_id=current_user.id)
    avg_rating_given = crud.rating.get_average_rating_by_user(db, user_id=current_user.id)

    return {
        "requests_created": requests_created,
        "requests_by_status": requests_by_status,
        "avg_rating_given": avg_rating_given,
    }
