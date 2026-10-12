"""
Code that tells the bot which prompt
to use, or call any other API, feature
available
"""

from ..services.ai import call_ai
from .personas import CHARS, char_list

text = str(call_ai(prompt))
