#Dependencies

import os
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

#app init

bolt_app = App(token=os.getenv("SLACK_BOT_TOKEN"),signing_secret=os.getenv("SLACK_SIGNING_SECRET"))

#functionality
@bolt_app.message("hi")
def reply(message,say):
  user = message['user']
  say(f"Hey <@{user}>! 👋")

#flask wrapper
flask_app = Flask(__name__)
handler = SlackRequestHandler(bolt_app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
