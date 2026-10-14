"""
Code that tells the bot which prompt
to use, or call any other API, feature
available
"""

from ..services.ai import call_ai
from ..services.slack import send_message, react

from .personas import CHARS, char_list
from .prompts.chat import respond
from .prompts.char_desc import desc

#text = str(call_ai(prompt))
async def think(context, data):
    char = CHARS["Iron"]
    
    char_prompt = desc(char)
    print(char_prompt)
    
    msg = await respond(
        #change to use names themselves
        char,
        data
    )
    return "hello"
#response.choices[0].message.content
