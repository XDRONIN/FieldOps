from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.rating import Rating
from app.schemas.rating import RatingCreate, RatingUpdate

class CRUDRating(CRUDBase[Rating, RatingCreate, RatingUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: RatingCreate, user_id: int
    ) -> Rating:
        db_obj = Rating(
            **obj_in.dict(),
            user_id=user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_average_rating(self, db: Session) -> float | None:
        from sqlalchemy import func
        return db.query(func.avg(Rating.rating)).scalar()

    def get_average_rating_by_user(self, db: Session, *, user_id: int) -> float | None:
        from sqlalchemy import func
        return db.query(func.avg(Rating.rating)).filter(Rating.user_id == user_id).scalar()

rating = CRUDRating(Rating)
