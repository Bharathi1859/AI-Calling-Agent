from faster_whisper import WhisperModel


class SpeechToText:

    def __init__(self):
        print("Loading Whisper model...")

        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

        print("Whisper model loaded successfully.")

    def transcribe(self, audio_file: str) -> str:
        segments, info = self.model.transcribe(
            audio_file,
            beam_size=5
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        return text.strip()