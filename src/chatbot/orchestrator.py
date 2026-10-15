"""
Code that tells the bot which prompt
to use, or call any other API, feature
available
"""

import random
from ..services.ai import call_ai
from ..services.slack import get_chat,send_message,PAGE_LENGTH

from .personas import CHARS
from .prompts.chat import respond
from .prompts.char_desc import desc

async def nothing2(chat,data):
    return False
    
async def nothing(chat,data,res):
    return False

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
        (lambda a,b: False), 
        (lambda a,b,c: False)
    )
)

cchar = "Iron"
#text = str(call_ai(prompt))
async def think(context, data):
    decision = random.choices(
        actions,
        weights=[
            40,
            20,
            20
        ],
        k=1
    )[0]

    char = CHARS[cchar]
    
    char_prompt = desc(char)
    
    msg = await decision[0](
        char_prompt,
        data
    )

    print(msg)

    global cchar
    if cchar=="Iron":
        cchar="Nancy"
    else:
        cchat="Iron"
        
    if msg != False:
        res = call_ai(msg)
        txt = res.choices[0].message.content
        await decision[1](
            char,data,txt
        )

        return True
#response.choices[0].message.content
