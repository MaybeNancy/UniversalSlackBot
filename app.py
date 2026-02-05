#new api
#dependencies
from flask import Flask, request, jsonify, abort
import requests
import os
import hmac
import hashlib

#init
app = Flask(__name__)
ADMIN = "U0AAS5ZGSAD"

# Environment variables for your Slack Token and Signing Secret
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')

# Function to verify Slack request signatures
def IsValidRequest(req):
    slack_signature = req.headers['X-Slack-Signature']
    request_body = req.get_data().decode('utf-8')
    timestamp = req.headers['X-Slack-Request-Timestamp']
    
    # Create the basestring
    basestring = f"v0:{timestamp}:{request_body}"
    
    # Generate the HMAC SHA256 hash of the basestring
    my_signature = 'v0=' + hmac.new(
        key=bytes(SLACK_SIGNING_SECRET, 'utf-8'),
        msg=bytes(basestring, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(my_signature, slack_signature)

# Function to send a message to a Slack channel
def SendMessage(channel_id, text):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Authorization': f'Bearer {SLACK_BOT_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'channel': channel_id,
        'text': text
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Endpoint to handle Slack events
@app.route('/slack/events', methods=['POST'])
def slack_events():
    if not IsValidRequest(request):
        abort(400)  # Invalid request if verification fails

    data = request.json
    channel_id = data['event']['channel']
    user_id = data['event']['user']

    #if user_id == ADMIN:
    SendMessage(channel_id, data)
    """
    
    
    # Respond to the challenge verification
    if 'challenge' in data:
        return jsonify({'challenge': data['challenge']})
    
    # Handle other events here
    event_type = data.get('event', {}).get('type')
    if event_type == 'message' and 'subtype' not in data['event']:
        user_id = data['event']['user']
        
        text = data['event']['text']
        SendMessage(channel_id, f"Hello <@{user_id}>, you said: {text}")
    """
    return jsonify({'status': 'ok'})

# Slash command endpoint
@app.route('/slack/commands', methods=['POST'])
def slack_commands():

    if not IsValidRequest(request):
        abort(400)
        
    data = request.form
    command = data.get("command")
    text = data.get("text")
    user_id = data.get("user_id")
    channel = data.get("channel_id")

    response_text = data

    SendMessage(channel,response_text)

    return jsonify({"response_type": "in-channel", "text": "🧠👍"})
