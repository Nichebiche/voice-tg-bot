import random

from aiogram import Router, types, F
from aiogram.filters.command import Command
from openai_client import convert_speech_to_text, get_openai_response, convert_text_to_speech

router = Router()

@router.message(Command("start"))
async def handle_start_command(message: types.Message):
    await message.answer("Let me hear you")

@router.message(F.voice)
async def handle_voice_message(message: types.Message):
    voice = message.voice
    file_info = await message.bot.get_file(voice.file_id)
    file_path = file_info.file_path
    file_url = f'https://api.telegram.org/file/bot{message.bot.token}/{file_path}'

    # TODO remove
    await message.answer(random.choice(["What?", "I can't hear you", "Come again?"]))
    await message.answer(f"Btw, it's link to your voice: {file_url}")
    return

    text = await convert_speech_to_text(file_url)
    await message.answer(f"You said: {text}")

    response_text = await get_openai_response(text)
    await message.answer(f"The answer: {response_text}")

    audio_data = await convert_text_to_speech(response_text)
    await message.answer_voice(audio=audio_data)