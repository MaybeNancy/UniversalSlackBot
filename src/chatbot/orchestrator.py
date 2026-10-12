"""
Code that tells the bot which prompt
to use, or call any other API, feature
available
"""

from ..services.ai import call_ai

text = str(call_ai(prompt))
