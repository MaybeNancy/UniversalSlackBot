"""
Code that tells the bot which prompt
to use, or call any other API, feature
available
"""

import random
from ..services.ai import call_ai
from ..services.slack import send_message,react,PAGE_LENGTH

from .personas import CHARS, char_list
from .prompts.chat import respond
from .prompts.char_desc import desc

async def nothing():
    return {"status":"ok"}

async def chat(char,data,res):
   return await send_message(
        char["img"],
        char["name"],
        data["channel"],
        res
    )
    
active = 1
actions = {
    {
        "func":respond, 
        "slack":chat
    },
    {
        "func":react, 
        "slack":nothing
    },
    {
        "func":nothing, 
        "slack":nothing
    }
}

async def activity(data):
    return 1
    
#text = str(call_ai(prompt))
async def think(context, data):
    active = (await activity(data))/PAGE_LENGTH

    decision = random.choices(
        actions["func"],
        weights=[
            (60*active),
            30-(30*active),
            5-(5*active)
        ],
        k=1
    )[0]
    
    char = CHARS["Iron"]
    
    char_prompt = desc(char)
    act = actions[decision][0]
    
    msg = await act["func"](
        char_prompt,
        data
    )

    res = call_ai(msg)
    txt = res.choices[0].message.content
    await actions["slack"](
        char,data,txt
    )

    return True
#response.choices[0].message.content
