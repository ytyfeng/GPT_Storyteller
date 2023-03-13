import os
import datetime
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
messages = []

class Message:
    def __init__(self, sender, text):
        self.sender = sender
        self.text = text
        self.timestamp = datetime.datetime.now()

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        userStory = request.form["user_story"]
        msgUser = Message("USER", userStory)
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
        msgAI = Message("AI", response.choices[0].text)
        messages.append(msgAI)
        return redirect(url_for("index"))
        #return redirect(url_for("index", result=response.choices[0].text))

    #result = request.args.get("result")
    return render_template("index.html", messages=messages)


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
