import os
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
import shutil
from app.core.config import get_settings
from app.models.user import Role

router = APIRouter()

@router.post("/assign", response_model=schemas.Task)
def assign_task(
    *,
    db: Session = Depends(deps.get_db),
    task_in: schemas.TaskCreate,
    current_user: models.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Assign a service request to a worker.
    """
    request = crud.service_request.get(db=db, id=task_in.request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Service request not found")
    worker = crud.user.get(db=db, id=task_in.worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    if worker.role != models.user.Role.WORKER:
        raise HTTPException(status_code=400, detail="This user is not a worker")

    task = crud.task.create_with_request_and_worker(db=db, obj_in=task_in)
    return task

@router.get("/", response_model=List[schemas.Task])
def read_tasks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_worker_or_admin),
) -> Any:
    """
    Retrieve tasks for the current worker.
    For admin return all tasks.
    """
    if current_user.role == models.user.Role.ADMIN:
        tasks = crud.task.get_multi(db=db, skip=skip, limit=limit)
    else:    
        tasks = crud.task.get_multi_by_worker(
        db=db, worker_id=current_user.id, skip=skip, limit=limit
    )
    return tasks

@router.patch("/{id}/status", response_model=schemas.Task)
def update_task_status(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    status_in: schemas.TaskStatusUpdate,
    current_user: models.User = Depends(deps.get_current_active_worker_or_admin),
) -> Any:
    """
    Update task status.
    """
    task = crud.task.get(db=db, id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role == models.user.Role.WORKER and task.worker_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    task_update = schemas.TaskUpdate(status=status_in.status)
    task = crud.task.update(db=db, db_obj=task, obj_in=task_update)

    if task.status == models.task.TaskStatus.COMPLETED:
        service_request = crud.service_request.get(db=db, id=task.request_id)
        if service_request:
            crud.service_request.update(
                db=db,
                db_obj=service_request,
                obj_in={"status": models.service_request.RequestStatus.COMPLETED},
            )

    return task

@router.post("/{id}/proof", response_model=schemas.Task)
def upload_proof(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    notes: str = Form(...),
    photo: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_worker),
) -> Any:
    """
    Upload proof of completion.
    """
    task = crud.task.get(db=db, id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.worker_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    settings = get_settings()
    # Create upload directory if it does not exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    # Save the photo
    file_path = f"{settings.UPLOAD_DIR}/{photo.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    task_update = schemas.TaskUpdate(proof_notes=notes, proof_photos=file_path)
    task = crud.task.update(db=db, db_obj=task, obj_in=task_update)
    return task
