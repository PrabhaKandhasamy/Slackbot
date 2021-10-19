import slack_sdk
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack_sdk.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']
# client.chat_postMessage(channel='#comcast', text="Hello ennoda kadavul oru paithiyam!")

@slack_event_adapter.on('message')        
def messgae(payLoad):
    print(payLoad)
    event = payLoad.get('event',{})
    channelId = event.get('channel')
    userId = event.get('user')
    text = event.get('text');
    if BOT_ID != userId:
        client.chat_postMessage(channel= channelId, text=text)
if __name__ == "__main__":
      app.run(debug=True)
