"""
I will modify this later, 
I just need the thing working
"""

import src.services.slack_service

def reply(data):
    # Example handler: respond "pong" when bot is mentioned
    channel = data["event"]["channel"]
    send_message(channel, "Hey")

    return {"status":"ok"}
    # Use ctx.logger if present; fallback to ctx.slack.logger
