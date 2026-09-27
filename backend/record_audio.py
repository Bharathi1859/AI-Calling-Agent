import sounddevice as sd
import soundfile as sf


DURATION = 10
SAMPLE_RATE = 16000
OUTPUT_FILE = "test_audio/customer_message.wav"


print("Recording will start now...")
print("Speak clearly for 10 seconds.")
print("Example: We need a commercial RO system with a capacity of 500 LPH.")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32"
)

sd.wait()

sf.write(
    OUTPUT_FILE,
    audio,
    SAMPLE_RATE
)

print()
print("Recording completed!")
print(f"Audio saved to: {OUTPUT_FILE}")