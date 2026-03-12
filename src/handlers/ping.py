"""
I will modify this later, 
I just need the thing working
"""

from ..services.slack_service import send_message

def reply(data):
    # Example handler: respond "pong" when bot is mentioned
    channel = data["channel"]
    send_message(channel, "Hey")

    return {"status":"ok"}
    # Use ctx.logger if present; fallback to ctx.slack.logger
