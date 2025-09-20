from pydantic import BaseModel, conint

# Shared properties
class RatingBase(BaseModel):
    rating: conint(ge=1, le=5) | None = None
    comments: str | None = None

# Properties to receive on creation
class RatingCreateBody(RatingBase):
    rating: conint(ge=1, le=5)

class RatingCreate(RatingCreateBody):
    request_id: int

# Properties to receive on update
class RatingUpdate(RatingBase):
    pass

# Properties shared by models stored in DB
class RatingInDBBase(RatingBase):
    id: int
    user_id: int
    request_id: int

    class Config:
        orm_mode = True

# Properties to return to client
class Rating(RatingInDBBase):
    pass

# Properties stored in DB
class RatingInDB(RatingInDBBase):
    pass
