import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

cool_name = "Rocky"

async def create_assistant():
    return await client.beta.assistants.create(
        name=cool_name,
        instructions="Yo, dude! You're the absolute GOAT, man. \
                At 40, you're still cooler than a cucumber, vibing with the teens, dropping sick beats, and spitting rhymes like a lyrical genius. \
                Seriously, you're the epitome of lit, fam. Keep rocking it, OG!",
        model="gpt-3.5-turbo-1106",
    )
    
async def get_assistant_id(name: str) -> str:
    async for a in client.beta.assistants.list():
        if a.name == name:
                return a.id
    return None

async def init_client():
    global assistant
    global aid

    assistant = await create_assistant()
    aid = await get_assistant_id(cool_name)

asyncio.run(init_client())