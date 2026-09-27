from app.voice.tts import TextToSpeech


tts = TextToSpeech()

text = (
    "Thank you for providing the information. "
    "We will review your requirement and get back to you."
)

output_file = "test_audio/agent_response.mp3"

print("Generating speech...")

tts.synthesize(
    text=text,
    output_file=output_file
)

print("Speech generated successfully!")
print(f"Audio saved to: {output_file}")