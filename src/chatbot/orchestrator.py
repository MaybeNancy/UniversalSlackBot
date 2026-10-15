"""
Code that tells the bot which prompt
to use, or call any other API, feature
available
"""

import random
from ..services.ai import call_ai
from ..services.slack import get_chat,send_message,presence

from ..globals import r_nancy

from .personas import CHARS
from .prompts.chat import respond
from .prompts.char_desc import desc

async def checknancy():
    res = await presence(r_nancy())

    print(res)
    if res["presence"] == "active":
        return "Iron"
    else:
        return "Nancy"

def range(x,a,b):
    if(x>=a) and (x<=b):
        return True
    else:
        return False

async def think(context, data):
    r = random.random()

    if r>=0 and r<=0:
        char = CHARS[await checknancy()]
        char_prompt = desc(char)

        msg = respond(
            char_prompt,
            data
        )

        print(msg)
        
        if msg != 0:
            res = call_ai(msg)
            txt = res.choices[0].message.content
            await decision[1](
                char,data,txt
            )

        return await send_message(
            char["name"],
            char["img"],
            data["channel"],
            res
        )

        return True
        
    elif r>=0 and r<=0:
        char_prompt = desc(CHARS["Iron"])
        return True
    return False
    
