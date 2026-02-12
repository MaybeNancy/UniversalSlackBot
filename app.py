#new api
#dependencies
from flask import Flask, request, jsonify, abort
import requests
import os
import hmac
import hashlib
import datetime
import random

#init
app = Flask(__name__)
ADMIN = "U0AAS5ZGSAD"
BOT = "U0ABJJQ288M"
DFT_CHANNEL = "C0AC0154XSL"

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

def SendMedia(channel_id,img_url,video_url,is_video):
    if is_video:
        sprint(is_video)
        sprint(video_url)
        blocks = [
            {
                "type":"video",
                "alt_text":"text",
                "title":{
                    "type":"plain_text",
                    "text" :"a movie for you. :>"
                },
                "thumbnail_url":img_url,
                "video_url":video_url
            }
        ]
    else:
        blocks = [
            {
                "type":"image",
                "title": {
                    "type": "plain_text",
                    "text": "Please enjoy this photo :>"
                },
                "alt_text":"img",
                "image_url":img_url
            }
        ]
    
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Authorization': f'Bearer {SLACK_BOT_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'channel': channel_id,
        'blocks': blocks,
        'username': "Brian🧠"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

#quick slack chat print for debuggin'
def sprint(text):
    SendMessage(DFT_CHANNEL,text)

def EncText(text):
    return text.encode("unicode_escape").decode("utf-8")

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
        #SendMessage(channel_id, data)

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
        'access_token': DA_token
    }
    
    response = requests.get(url, params=params).json()
    
    #sprint(response)
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
    
        response = requests.get(url, params=params).json()
        global DA_token
        DA_token = response["access_token"]

#get user's gallery
def GetDAGall(user):
    url = "https://www.deviantart.com/api/v1/oauth2/gallery/all"
    params = {
        'access_token': DA_token,
        "username" : user,
        "mature_content": "true"
    }
    
    response = requests.get(url, params=params)
    return response.json()

#just normal search
def DASearch(search):
    url = "https://www.deviantart.com/api/v1/oauth2/browse/home"
    params = {
        'access_token': DA_token,
        "q" : search,
        "mature_content": "true",
        "limit":5,
        "offset":random.ranint(1,200)
    }
    
    response = requests.get(url, params=params)
    return response.json()

def DATag(tag):
    url = "https://www.deviantart.com/api/v1/oauth2/browse/tags"
    params = {
        'access_token': DA_token,
        "tag" : tag,
        "mature_content": "true",
        "limit":5,
        "offset":4
    }
    
    response = requests.get(url, params=params)
    return response.json()

#TODO, DA FETCH VIA LINK
#def DAlink(link)
def DAShow(channel, deviation):
    videos = deviation.get("videos")
    src = deviation["preview"]["src"]
    if videos != None:
        for v in videos:
            vsrc = v["src"]
            SendMedia(channel,src,vsrc,True)
    else:
        SendMedia(channel,src,None,False)
    
"""
type 0 for normal search
type 1 for user
type 2 for tag
type 3 for url
"""

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

    entxt = EncText(text)

    #endMessage(channel,command)

    if command == "/echo":
        b_msg = SendMessage(channel,text)
        global perm_bot_msg 
        perm_bot_msg = b_msg["ts"]
    elif command == "/da":
        GetDA()
        search_mode = 0

        if entxt.find("@") == 0:
            search_mode=1
        elif entxt.find("#") == 0:
            search_mode=2
        elif entxt.startswith("https://"):
            search_mode=3

        if search_mode==0:
            searches = DASearch(entxt)["results"]
            for i in searches:
                DAShow(channel, i)
        elif search_mode==1:
            user = entxt.replace("@","")
            gallery = GetDAGall(user)["results"]

            for i in gallery:
                DAShow(channel, i)
        elif search_mode==2:
            tag = entxt.replace("#","")
            tags = DATag(tag)["results"]

            for i in tags:
                DAShow(channel, i)

    return jsonify({"response_type": "ephemeral", "text": "Done! 🧠👍"})
