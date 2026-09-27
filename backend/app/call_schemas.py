from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CallCreate(BaseModel):
    customer_id: int


class CallResponse(BaseModel):
    id: int
    customer_id: int
    provider_call_id: str | None
    direction: str
    status: str
    start_time: datetime | None
    end_time: datetime | None
    duration: int | None
    outcome: str | None
    lead_status: str | None
    follow_up_required: str
    error_message: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)