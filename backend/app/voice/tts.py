import asyncio

import edge_tts


class TextToSpeech:

    def __init__(self):
        self.voice = "en-US-AriaNeural"

    async def generate_audio(
        self,
        text: str,
        output_file: str
    ):
        communicate = edge_tts.Communicate(
            text,
            self.voice
        )

        await communicate.save(output_file)

    def synthesize(
        self,
        text: str,
        output_file: str
    ):
        asyncio.run(
            self.generate_audio(
                text,
                output_file
            )
        )