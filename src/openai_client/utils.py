import json
import logging 
from . import client
from config import TEMP_DIR

async def save_messages_to_temp(thread_id: int) -> None:
    messages = await client.beta.threads.messages.list(thread_id=thread_id)
    
    messages_dict = messages.to_dict() if hasattr(messages, 'to_dict') else messages
    temp_file_path = TEMP_DIR / f"messages_{thread_id}.json"

    with open(temp_file_path, 'w') as f:
        json.dump(messages_dict, f, indent=4)

    logging.info(f"Messages for thread {thread_id} saved to {temp_file_path}")
