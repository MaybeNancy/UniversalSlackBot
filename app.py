#new api
#dependencies
from flask import Flask, request, jsonify, abort
import requests
import os
import hmac
import hashlib
import datetime

#init
app = Flask(__name__)
ADMIN = "U0AAS5ZGSAD"
BOT = "U0ABJJQ288M"

perm_bot_msg = ""
DA_token = "NA"

# Environment variables for your Slack Token and Signing Secret
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
SLACK_USER_TOKEN = os.getenv('SLACK_USER_TOKEN')

#DeviantArt
DA_API_ID = os.getenv('DA_API_ID')
DA_API_SECRET = os.getenv('DA_API_SECRET')

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

#deletes message inmediately
def DelMessage(token, channel_id,timestamp):
    url = "https://slack.com/api/chat.delete"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        "channel" : channel_id,
        "ts" :timestamp
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()
    
# Function to send a message to a Slack channel
def SendMessage(channel_id,text):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Authorization': f'Bearer {SLACK_BOT_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'channel': channel_id,
        'text': text,
        'username': "Brian🧠"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def EncText(text):
    return text.encode("unicode_escape").decode("utf-8")

#Removes commands as text
def CommDup(text,channel,ts):
    """
    TODO: Implememt a parser that searches for 
    custom commands written at first (attempting
    to do a command as plain text), otherwise is just
    normal text mentioning a command

    NOT NEEDED, BUT SAVE IF LOGIC BECOMES USEFUL
    """
    text_batch = text.split(" ")
    slash_loc = text_batch[0].find("/")
    
    if slash_loc == 0:
        DelMessage(SLACK_BOT_TOKEN,channel,ts)
        DelMessage(SLACK_USER_TOKEN,channel,ts)

# Endpoint to handle Slack events
@app.route('/slack/events', methods=['POST'])
def slack_events():
    if not IsValidRequest(request):
        abort(400)  # Invalid request if verification fails

    data = request.json
    channel_id = data['event']['channel']
    user_id = data['event']['user']
    ts = data['event']['ts']
    text = data['event']['text']
    entxt = EncText(text)
    txt = user_id+f"Bearer {perm_bot_msg}"

    #CommDup(entxt,channel_id,ts)
    
    #if user_id == ADMIN:
        #SendMessage(channel_id, entxt)

    #elif
    
    
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


#check if da token still valid after 1 hour
def CheckDAToken():
    url = "https://www.deviantart.com/api/v1/oauth2/placebo"

    params = {
        'client_id': DA_API_ID,
        "client_secret" : DA_API_SECRET,
        'grant_type': 'client_credentials'
    }
    
    response = requests.get(url, params=params).json()
    if response["status"] == "success":
        return True
    else:
        return False

#Getch DA deviation via username and/or title
def GetDA():
    if not CheckDAToken():
        url = "https://www.deviantart.com/oauth2/token"
        params = {
            'client_id': DA_API_ID,
            "client_secret" : DA_API_SECRET,
            'grant_type': 'client_credentials'
        }
    
        response = requests.get(url, params=params)
        return response.json()
    return DA_token

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

    #endMessage(channel,command)

    if command == "/echo":
        b_msg = SendMessage(channel,text)
        global perm_bot_msg 
        perm_bot_msg = b_msg["ts"]
    elif command == "/da":
        DA_token = GetDA()["token"]
        SendMessage(channel,DA_token)

    return jsonify({"response_type": "ephemeral", "text": "Done! 🧠👍"})
