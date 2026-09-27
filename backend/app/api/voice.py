import os
import shutil
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.call import Call
from app.models.conversation import ConversationMessage

from app.agent.agent import CallingAgent
from app.agent.state_service import (
    load_conversation_state,
    save_conversation_state
)

from app.voice.stt import SpeechToText
from app.voice.tts import TextToSpeech


router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)


UPLOAD_DIR = "test_audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/process/{call_id}")
async def process_voice(
    call_id: int,
    audio: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Find call
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

    # Create temporary audio filename
    file_extension = os.path.splitext(
        audio.filename or ".wav"
    )[1]

    input_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )

    input_path = os.path.join(
        UPLOAD_DIR,
        input_filename
    )

    # Save uploaded audio
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(
            audio.file,
            buffer
        )

    try:
        # -----------------------------
        # 1. Speech-to-Text
        # -----------------------------
        stt = SpeechToText()

        customer_text = stt.transcribe(
            input_path
        )

        if not customer_text:
            raise HTTPException(
                status_code=400,
                detail="Could not detect speech in audio"
            )

        # Save customer message
        customer_message = ConversationMessage(
            call_id=call_id,
            speaker="customer",
            message=customer_text
        )

        db.add(customer_message)
        db.commit()

        # -----------------------------
        # 2. Load conversation state
        # -----------------------------
        customer = call.customer

        state = load_conversation_state(
            db=db,
            call_id=call_id,
            customer_name=customer.name,
            company_name=customer.company_name,
            default_requirement=customer.product
        )

        agent = CallingAgent(state)

        # -----------------------------
        # 3. Gemini AI Agent
        # -----------------------------
        result = agent.process_message(
            customer_text
        )

        # Save updated state
        save_conversation_state(
            db=db,
            call_id=call_id,
            state=agent.state
        )

        # -----------------------------
        # 4. Text-to-Speech
        # -----------------------------
        output_filename = (
            f"{uuid.uuid4()}.mp3"
        )

        output_path = os.path.join(
            UPLOAD_DIR,
            output_filename
        )

        tts = TextToSpeech()

        await tts.generate_audio(
            text=result["agent_response"],
            output_file=output_path
)

        # Save AI response
        ai_message = ConversationMessage(
            call_id=call_id,
            speaker="ai",
            message=result["agent_response"]
        )

        db.add(ai_message)
        db.commit()

        return {
            "call_id": call_id,
            "customer_text": customer_text,
            "agent_response": result["agent_response"],
            "conversation_state": result["conversation_state"],
            "missing_fields": result["missing_fields"],
            "audio_file": output_path
        }

    finally:
        # Remove temporary input audio
        if os.path.exists(input_path):
            os.remove(input_path)