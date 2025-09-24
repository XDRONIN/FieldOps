from pydantic import BaseModel
from app.models.service_request import Urgency, RequestStatus

# Shared properties
class ServiceRequestBase(BaseModel):
    description: str | None = None
    location: str | None = None
    urgency: Urgency | None = None

# Properties to receive on creation
class ServiceRequestCreate(ServiceRequestBase):
    description: str
    location: str
    urgency: Urgency

# Properties to receive on update
class ServiceRequestUpdate(ServiceRequestBase):
    pass

from pydantic import ConfigDict

# Properties shared by models stored in DB
class ServiceRequestInDBBase(ServiceRequestBase):
    id: int
    user_id: int
    status: RequestStatus

    model_config = ConfigDict(from_attributes=True)

# Properties to return to client
class ServiceRequest(ServiceRequestInDBBase):
    pass

# Properties stored in DB
class ServiceRequestInDB(ServiceRequestInDBBase):
    pass
