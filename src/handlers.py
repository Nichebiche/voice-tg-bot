import logging
from aiogram import Bot, Router, types, F
from aiogram.types import FSInputFile
from aiogram.filters.command import Command
from openai_client.api import convert_speech_to_text, get_openai_response, convert_text_to_speech
from config import TEMP_DIR

router = Router()

@router.message(Command("start"))
async def handle_start_command(message: types.Message):
    await message.answer("Let me hear you")

@router.message(F.voice)
async def handle_voice_message(message: types.Message, bot: Bot):
    uid = message.from_user.id
    voice = message.voice
    voice_resp_path = TEMP_DIR / f"req_{uid}.mp3"
    await bot.download(voice, voice_resp_path)

    text = await convert_speech_to_text(voice_resp_path, uid)
    response_text = await get_openai_response(text, uid)
    voice_ans_path = await convert_text_to_speech(response_text, uid)
    
    if voice_ans_path is not None:
        logging.info(f"Sending voice to {uid}")
        await message.reply_voice(voice=FSInputFile(voice_ans_path))
    else:
        logging.error(f"Failed to create voice message for {uid}")