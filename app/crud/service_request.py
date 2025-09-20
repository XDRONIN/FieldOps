from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.service_request import ServiceRequest
from app.schemas.service_request import ServiceRequestCreate, ServiceRequestUpdate

class CRUDServiceRequest(CRUDBase[ServiceRequest, ServiceRequestCreate, ServiceRequestUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ServiceRequestCreate, user_id: int
    ) -> ServiceRequest:
        db_obj = ServiceRequest(
            **obj_in.dict(),
            user_id=user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[ServiceRequest]:
        return (
            db.query(self.model)
            .filter(ServiceRequest.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_requests_by_status_count_by_owner(self, db: Session, *, user_id: int) -> dict:
        from sqlalchemy import func
        return dict(
            db.query(ServiceRequest.status, func.count(ServiceRequest.id))
            .filter(ServiceRequest.user_id == user_id)
            .group_by(ServiceRequest.status)
            .all()
        )

service_request = CRUDServiceRequest(ServiceRequest)
