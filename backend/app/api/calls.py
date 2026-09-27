from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.call import Call
from app.models.customer import Customer
from app.call_schemas import CallCreate, CallResponse


router = APIRouter(
    prefix="/calls",
    tags=["Calls"]
)


@router.post(
    "",
    response_model=CallResponse,
    status_code=201
)
def create_call(
    call_data: CallCreate,
    db: Session = Depends(get_db)
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == call_data.customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    call = Call(
        customer_id=customer.id,
        direction="outbound",
        status="initiated",
        start_time=datetime.utcnow()
    )

    db.add(call)
    db.commit()
    db.refresh(call)

    return call


@router.get(
    "",
    response_model=list[CallResponse]
)
def get_calls(
    db: Session = Depends(get_db)
):
    calls = (
        db.query(Call)
        .order_by(Call.created_at.desc())
        .all()
    )

    return calls


@router.get(
    "/{call_id}",
    response_model=CallResponse
)
def get_call(
    call_id: int,
    db: Session = Depends(get_db)
):
    call = (
        db.query(Call)
        .filter(Call.id == call_id)
        .first()
    )

    if not call:
        raise HTTPException(
            status_code=404,
            detail="Call not found"
        )

    return call


@router.patch(
    "/{call_id}/status",
    response_model=CallResponse
)
def update_call_status(
    call_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    call = (
        db.query(Call)
        .filter(Call.id == call_id)
        .first()
    )

    if not call:
        raise HTTPException(
            status_code=404,
            detail="Call not found"
        )

    call.status = status

    if status == "completed":
        call.end_time = datetime.utcnow()

        if call.start_time:
            duration = (
                call.end_time - call.start_time
            ).total_seconds()

            call.duration = int(duration)

    db.commit()
    db.refresh(call)

    return call