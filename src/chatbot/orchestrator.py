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

actions = {
    "reply":respond#,
   # "react":react
    
}
#text = str(call_ai(prompt))
async def think(context, data):
    char = CHARS["Iron"]
    
    char_prompt = desc(char)
    action = action["reply"]  
    
    msg = await action(
        char_prompt,
        data
    )
    return "hello"
#response.choices[0].message.content
