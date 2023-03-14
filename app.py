import os
import datetime
import openai
from flask import Flask, redirect, render_template, request, url_for, make_response
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./gptstoryteller-firebase-adminsdk-bhz08-8514eb1c53.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

db = firestore.client()
collection = db.collection('messages')

class Message:
    def  __init__(self, sender, text, timestamp):
        self.sender = sender
        self.text = text
        self.timestamp = timestamp

def toDict(messages):
    dict = []
    for m in messages:
        dict.append(vars(m))
    return dict

def toMessages(dict):
    messages = []
    for d in dict:
        m = Message(d["sender"], d["text"], d["timestamp"])
        messages.append(m)
    return messages

@app.route('/messages/<uuid>', methods=['GET'])
def getMessages(uuid):
    cookieUUID = request.cookies.get('storyteller_id')
    if cookieUUID is None or cookieUUID == '':
        cookieUUID = uuid
    doc = collection.document(cookieUUID).get()
    messages = []
    if doc.exists:
        messages = toMessages(doc.to_dict().get("messages"))
    resp = make_response(render_template("index.html", messages=messages))
    resp.set_cookie('storyteller_id', cookieUUID, max_age=2592000)
    return resp

@app.route('/messages/<uuid>', methods=['POST'])
def saveMessages(uuid):
    uuid = request.cookies.get('storyteller_id')
    userStory = request.form["user_story"]
    msgUser = Message("USER", userStory, datetime.datetime.now())
    doc = collection.document(uuid).get()
    if doc.exists:
        messages = toMessages(doc.to_dict().get("messages"))
    else:
        messages = []
    messages.append(msgUser)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(messages),
        max_tokens=600,
        temperature=0.8,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    msgAI = Message("AI", response.choices[0].text, datetime.datetime.now())
    messages.append(msgAI)
    if doc.exists:
        collection.document(uuid).update({"messages" : toDict(messages)})
    else:
        collection.document(uuid).set({"messages" : toDict(messages)})
    return render_template("index.html", messages=messages)

@app.route('/removeCookie', methods=['GET'])
def removeCookie():
    resp = make_response(render_template("index.html"))
    resp.set_cookie('storyteller_id', expires=1)
    return resp

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

def generate_prompt(messages):
    story = ""
    for m in messages:
        story += m.text + " "
    return """Imagine you are an intelligent storyteller. Here is a part of a story.
    Generate the next story event based on the story. Make sure the eventual story is coherent. 
    Story so far: {}
    Completion:""".format(
        story
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
