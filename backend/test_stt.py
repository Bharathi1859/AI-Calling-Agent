from app.voice.stt import SpeechToText


audio_file = "test_audio/customer_message.wav"

print("Starting Speech-to-Text test...")

stt = SpeechToText()

text = stt.transcribe(audio_file)

print("\nTranscription:")
print(text)