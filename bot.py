import os
import random
from flask import Flask, json, request
import requests
import re


app = Flask(__name__)

def reply(message):
    print("Replying to group")
    payload = {
        'bot_id' : os.environ['BOT_ID'],
        'text'   : message,
    }
    requests.post('https://api.groupme.com/v3/bots/post', json=payload)


@app.route('/', methods=['POST','GET'])
def groupme_callback():
    print("Got Connection...parsing:")
    json_body = request.get_json()
    if json_body['group_id'] == os.environ['GROUP_ID'] and json_body['sender_type'] != 'bot':
        # some degree of verification that it is sent via a groupme callback
        # could also check for "User-Agent: GroupMeBotNotifier/1.0", but that's plenty spoofable

        message = json_body['text']
        if any(adam in message.lower().split() for adam in ["adam", "@adam"]):
                print("Adam found!")
                reply("Adam! https://thumbs.gfycat.com/HorribleEcstaticCuckoo-size_restricted.gif")
        else:
                print("Adam Not Found in: {}".format(message))
    else:
        print("Not from groupme!")
    return "ok", 200
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port, debug=True)
    app.run(host='0.0.0.0', port=port)
