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
from .prompts.unavailable import unavailable

async def checknancy():
    res = await presence(r_nancy())

    if res["presence"] == "active":
        return "Iron"
    else:
        return "Nancy"

def range(x,min,max):
    if(x>=min) and (x<=max):
        return True
    else:
        return False

async def think(context, data):
    r = random.random()

    if range(r,0.4,1) == True:
        char = CHARS[await checknancy()]
        char_prompt = desc(char)

        msg = await respond(
            char_prompt,
            data
        )

        if msg != False:
            res = call_ai(msg)
            if res != False:
                txt = res.choices[0].message.content

            else:
                txt = unavailable()
            return await send_message(
                char["name"],
                char["img"],
                data["channel"],
                txt
            )
        return False
        
    elif range(r,0.2,0.4) == True:
        char_prompt = desc(CHARS["Iron"])
        return False
    return False
