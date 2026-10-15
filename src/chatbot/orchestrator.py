"""
Code that tells the bot which prompt
to use, or call any other API, feature
available
"""

import random
from ..services.ai import call_ai
from ..services.slack import get_chat,send_message,presence

from .personas import CHARS
from .prompts.chat import respond
from .prompts.char_desc import desc

async def checknancy():
    res = await presence("U0AAS5ZGSAD")

    print(res["presence"])
    if res["presence"] == "active":
        return "Iron"
    else:
        return "Nancy"

async def chat(char,data,res):
   return await send_message(
       char["name"],
        char["img"],
        data["channel"],
        res
    )
    
actions = (
    (
        respond, 
        chat
    ),
    (
        respond, 
        chat
    ),
    (
        async (lambda a,b: False), 
        async (lambda a,b,c: False)
    )
)

async def think(context, data):
    decision = random.choices(
        actions,
        weights=[
            40,
            20,
            60
        ],
        k=1
    )[0]

    char = CHARS[checknancy()]
    
    char_prompt = desc(char)
    
    msg = await decision[0](
        char_prompt,
        data
    )

    print(msg)
        
    if msg != False:
        res = call_ai(msg)
        txt = res.choices[0].message.content
        await decision[1](
            char,data,txt
        )

        return True
#response.choices[0].message.content
