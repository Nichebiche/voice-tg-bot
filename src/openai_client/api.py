import logging
import aiofiles
from typing import Optional
from config import TEMP_DIR
from openai_client.logic import authenticate, run_assistant 
from . import client


async def convert_speech_to_text(mp3_file_path : str, uid : int) -> str:
    with open(mp3_file_path, "rb") as audio_file:
        translation = await client.audio.translations.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    
    logging.info(f"User {uid} said: {translation}")
    return translation


async def get_openai_response(prompt: str, uid : int) -> str:
    tid = await authenticate(uid)
    
    await client.beta.threads.messages.create(
        thread_id=tid,
        content=prompt, 
        role='user'
    )
    
    response = await run_assistant(tid)
    
    logging.info(f"User {uid} heard: {response}")
    return response


async def convert_text_to_speech(text: str, uid : int) -> Optional[str]:
    mp3_file_path = TEMP_DIR / f"ans_{uid}.mp3"
    
    async with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="onyx",
        input=text
    ) as response:
        async with aiofiles.open(mp3_file_path, 'wb') as f:
            async for chunk in response.iter_bytes():
                await f.write(chunk)
    
    if mp3_file_path.exists() and mp3_file_path.stat().st_size > 0:
        return mp3_file_path
    else:
        return None
