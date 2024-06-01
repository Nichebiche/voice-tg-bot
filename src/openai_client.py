import aiohttp
import openai
from io import BytesIO

async def convert_speech_to_text(file_url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            audio_data = await resp.read()

        audio_file = BytesIO(audio_data)
        transcription = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file
        )
        return transcription['text']

async def get_openai_response(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

async def convert_text_to_speech(text: str) -> bytes:
    from pathlib import Path

    speech_file_path = Path("/tmp/temp_speech.mp3")
    response = openai.Audio.create(
        model="tts-1",
        voice="onyx",
        input=text
    )
    response.stream_to_file(speech_file_path)

    with open(speech_file_path, "rb") as speech_file:
        speech_data = speech_file.read()

    return speech_data
