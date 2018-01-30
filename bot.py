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
        if re.compile("^/oddsbot [1-9][0-9]*$").match(message):
                print("Message passes regex")
                (myname, maxval) = message.split(" ")
                maxval = int(maxval) + 1
                r1 = random.randrange(1,maxval)
                r2 = random.randrange(1,maxval)
                r3 = random.randrange(1,maxval)
                r4 = random.randrange(1,maxval)
                response = "3, 2, 1...{}! {}!".format(r1,r2)
                if r1 == r2:
                        #case where you lose
                        response += "\nYou Lose!"
                else:
                        response += "\nThrowback: 3, 2, 1...{}! {}!".format(r3,r4)
                        if r3 == r4:
                                #case where they lose
                                response += "\nThey Lose!"
                        else:
                                response += "\nPhew!"
                reply(response)
        else:
                print("Message doesn't match regex: {}".format(message))
    else:
        print("Not from groupme!")
    return "ok", 200
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port, debug=True)
    app.run(host='0.0.0.0', port=port)
