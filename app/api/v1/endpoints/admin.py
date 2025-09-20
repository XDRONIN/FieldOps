from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas as base_schemas
from app.schemas import admin as admin_schemas
from app.api import deps

router = APIRouter()

@router.get("/users", response_model=List[base_schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users

@router.patch("/users/{user_id}/status", response_model=base_schemas.User)
def update_user_status(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: admin_schemas.UserStatusUpdate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Update a user's status (activate/deactivate).
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user

@router.patch("/workers/{worker_id}/approval", response_model=base_schemas.User)
def update_worker_approval(
    *,
    db: Session = Depends(deps.get_db),
    worker_id: int,
    worker_in: admin_schemas.WorkerApprovalUpdate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Approve or reject a field worker.
    """
    worker = crud.user.get(db, id=worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    if worker.role != models.user.Role.WORKER:
        raise HTTPException(status_code=400, detail="This user is not a worker")
    worker = crud.user.update(db, db_obj=worker, obj_in=worker_in)
    return worker
