import g4f
import g4f.Provider
from g4f.models import *
from g4f.providers.retry_provider import IterListProvider

providers = IterListProvider([Blackbox, ChatGptEs, PollinationsAI, DarkAI, ChatGpt, 
                              GigaChat, Airforce, Liaobots, OpenaiChat], shuffle=False)

async def ask_gpt(promt : str) -> str:
    response = await g4f.ChatCompletion.create_async(
        model=gpt_4o,
        provider=providers,
        messages=[{'role': 'user', 'content': promt}],
    ) 