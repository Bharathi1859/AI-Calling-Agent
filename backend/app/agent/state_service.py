from sqlalchemy.orm import Session

from app.agent.state import ConversationState
from app.models.summary import CallSummary


def load_conversation_state(
    db: Session,
    call_id: int,
    customer_name: str,
    company_name: str,
    default_requirement: str | None = None
):
    summary = (
        db.query(CallSummary)
        .filter(CallSummary.call_id == call_id)
        .first()
    )

    if summary:
        state = ConversationState(
            customer_name=customer_name,
            company_name=company_name,
            requirement=summary.requirement
        )

        state.capacity = summary.capacity
        state.location = summary.location
        state.application = summary.application
        state.budget = summary.budget
        state.timeline = summary.timeline

        return state

    return ConversationState(
        customer_name=customer_name,
        company_name=company_name,
        requirement=default_requirement
    )


def save_conversation_state(
    db: Session,
    call_id: int,
    state: ConversationState
):
    summary = (
        db.query(CallSummary)
        .filter(CallSummary.call_id == call_id)
        .first()
    )

    if not summary:
        summary = CallSummary(call_id=call_id)
        db.add(summary)

    summary.requirement = state.requirement
    summary.capacity = state.capacity
    summary.location = state.location
    summary.application = state.application
    summary.budget = state.budget
    summary.timeline = state.timeline

    db.commit()
    db.refresh(summary)

    return summary