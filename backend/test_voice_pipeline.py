from app.agent.state import ConversationState
from app.agent.agent import CallingAgent
from app.voice.stt import SpeechToText
from app.voice.tts import TextToSpeech


AUDIO_INPUT = "test_audio/customer_message.wav"
AUDIO_OUTPUT = "test_audio/agent_response.mp3"


print("\n========== AI VOICE PIPELINE ==========\n")


# 1. Speech-to-Text
print("Step 1: Converting customer voice to text...")

stt = SpeechToText()

customer_text = stt.transcribe(
    AUDIO_INPUT
)

print("\nCustomer said:")
print(customer_text)


# 2. Create AI Agent
print("\nStep 2: Starting AI Agent...")

state = ConversationState(
    customer_name="Rahul Kumar",
    company_name="ABC Hotels"
)

agent = CallingAgent(state)


# 3. Process customer message
print("\nStep 3: Processing customer message with Gemini...")

result = agent.process_message(
    customer_text
)

print("\nAI Response:")
print(result["agent_response"])

print("\nConversation State:")
print(result["conversation_state"])

print("\nMissing Fields:")
print(result["missing_fields"])


# 4. Text-to-Speech
print("\nStep 4: Converting AI response to speech...")

tts = TextToSpeech()

tts.synthesize(
    text=result["agent_response"],
    output_file=AUDIO_OUTPUT
)

print("\nAI voice generated successfully!")
print(f"Audio saved to: {AUDIO_OUTPUT}")


print("\n========== PIPELINE COMPLETED ==========\n")