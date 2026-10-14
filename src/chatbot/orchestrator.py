"""
Code that tells the bot which prompt
to use, or call any other API, feature
available
"""

import random
from ..services.ai import call_ai
from ..services.slack import send_message, react

from .personas import CHARS, char_list
from .prompts.chat import respond
from .prompts.char_desc import desc

actions = {
    "reply":respond#,
   # "react":react
    
}
#text = str(call_ai(prompt))
async def think(context, data):
    if random.randint(0,3) == 3:
     char = CHARS["Iron"]
    
     char_prompt = desc(char)
     act = actions["reply"]  
    
     msg = await act(
        char_prompt,
        data
     )

     res = call_ai(msg)
     txt = res.choices[0].message.content
     slack = await send_message(
        char["img"],
        char["name"],
        data["channel"],
        txt
     )
     return True
#response.choices[0].message.content
