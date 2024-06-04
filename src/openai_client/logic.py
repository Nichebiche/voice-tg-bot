import shelve
import asyncio
import logging 
from . import client, aid   
from openai_client.utils import save_messages_to_temp
from config import DB_DIR   
    
def check_if_thread_exists(uid: int):
    with shelve.open(DB_DIR / "sessions.db") as sessions:
        return sessions.get(str(uid), None)


def store_thread(uid: int, thread_id: int):
    with shelve.open(DB_DIR / "sessions.db", writeback=True) as sessions:
        sessions[str(uid)] = thread_id
        logging.info(f"Thread {thread_id} created for user {uid}")


async def authenticate(uid: int) -> int:
    tid = check_if_thread_exists(uid)
    
    if tid is None:
        thread = await client.beta.threads.create()
        store_thread(uid, thread.id)
        tid = thread.id
    
    return tid


async def run_assistant(tid: int) -> str:
    run = await client.beta.threads.runs.create(thread_id=tid, assistant_id=aid)

    while run.status != "completed":
        await asyncio.sleep(0.5)
        run = await client.beta.threads.runs.retrieve(thread_id=tid, run_id=run.id)

    messages = await client.beta.threads.messages.list(thread_id=tid)
    
    await save_messages_to_temp(tid)
    
    response = messages.data[0].content[0].text.value
    return response
