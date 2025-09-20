from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.ServiceRequest)
def create_service_request(
    *,
    db: Session = Depends(deps.get_db),
    request_in: schemas.ServiceRequestCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new service request.
    """
    request = crud.service_request.create_with_owner(
        db=db, obj_in=request_in, user_id=current_user.id
    )
    return request

@router.get("/", response_model=List[schemas.ServiceRequest])
def read_service_requests(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve service requests for the current user.
    """
    if current_user.role == models.user.Role.ADMIN:
        requests = crud.service_request.get_multi(db, skip=skip, limit=limit)
    else:
        requests = crud.service_request.get_multi_by_owner(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return requests

@router.get("/{id}", response_model=schemas.ServiceRequest)
def read_service_request(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get service request by ID.
    """
    request = crud.service_request.get(db=db, id=id)
    if not request:
        raise HTTPException(status_code=404, detail="Service request not found")
    if current_user.role != models.user.Role.ADMIN and (request.user_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return request

@router.put("/{id}/rate", response_model=schemas.Rating)
def rate_service_request(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    rating_in: schemas.rating.RatingCreateBody,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Rate a completed service request.
    """
    request = crud.service_request.get(db=db, id=id)
    if not request:
        raise HTTPException(status_code=404, detail="Service request not found")
    if request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if request.status != models.service_request.RequestStatus.COMPLETED:
        raise HTTPException(
            status_code=400, detail="Service request is not completed"
        )

    # a user can only rate a request once
    if request.rating:
        raise HTTPException(
            status_code=400, detail="Service request has already been rated"
        )

    rating_create = schemas.RatingCreate(request_id=id, **rating_in.dict())
    rating = crud.rating.create_with_owner(
        db=db, obj_in=rating_create, user_id=current_user.id
    )
    return rating
