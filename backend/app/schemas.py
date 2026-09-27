from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CustomerCreate(BaseModel):
    name: str
    phone: str
    company_name: str | None = None
    purpose: str | None = None
    product: str | None = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    company_name: str | None
    purpose: str | None
    product: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)