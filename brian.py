#Dependencies

import os
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

#app init

def require_env(name):
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing environment variable: {name}")
    return val

bolt_app = App(
    token=require_env("SLACK_BOT_TOKEN"),
    signing_secret=require_env("SLACK_SIGNING_SECRET")
)

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

app = flask_app
