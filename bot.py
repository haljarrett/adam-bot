import os
import random
from flask import Flask, json, request
import requests
import re
import time

app = Flask(__name__)

lastTime = -3600

# New responses added here and are then passed to the reply function.
response_dict = {
    'adam' : {
        'text'     : "Adam!",
        'cooldown' : 3600,
        'url'      : 'https://i.groupme.com/368x368.gif.0ddac4592b7840ca9bc78adf619ac928'
    },
    '@adam' : {
        'text'     : "Adam!",
        'cooldown' : 3600,
        'url'      : 'https://i.groupme.com/368x368.gif.0ddac4592b7840ca9bc78adf619ac928'
    }
}

def reply(key):
    print("Replying to group")

    # Pulls the response info
    response_values = response_dict[key]

    payload = {
        'bot_id'      : os.environ['BOT_ID'],
        'text'        : response_values['text'],
        'attachments' : [
            {
                'type' : 'image',
                'url'  : response_values['url']
            }
        ]
    }
    requests.post('https://api.groupme.com/v3/bots/post', json=payload)

def scan_for_key(message):
    # Pulls every key out of the response dict
    # Searches for a match
    # If it finds one returns
    # If it goes through the whole dict and finds nothing returns null/none
    for key in response_dict:
        if message == key:
            return key

    return None

def check_cooldown(key):
    return time.clock() - lastTime > response_dict[key]['cooldown']

@app.route('/', methods=['POST','GET'])
def groupme_callback():
    global lastTime
    print("Got Connection...parsing:")

    json_body = request.get_json()
    # some degree of verification that it is sent via a groupme callback
    # could also check for "User-Agent: GroupMeBotNotifier/1.0", but that's plenty spoofable

    if json_body['group_id'] == os.environ['GROUP_ID'] and json_body['sender_type'] != 'bot':
        # Grab message body
        message = json_body['text']

        # Found key array in case we have so many responses it has multiple
        keys_found = []
        # Splits the message into an array
        substrings = message.lower().split + json_body['name'].lower().split()

        # Scans
        for substring in substrings:
            found_key = scan_for_key(substring)
            if found_key:
                keys_found.append(found_key)

        # Was a key found?
        if keys_found != []:
            # Selects a random key from the selection of keys
            choice = random.randint(0, len(keys_found))
            chosen_key = keys_found[choice]

            # Checks cooldown
            if check_cooldown(chosen_key):
                print(chosen_key + " found!")
                reply(chosen_key)
            else:
                print("Response is on cooldown: ".format(message))
        else:
            print("No response found in: ".format(message))
    else:
        print("Not from groupme!")

    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    # Uncomment for debugging
    # app.run(host='0.0.0.0', port=port, debug=True)
    app.run(host='0.0.0.0', port=port)
