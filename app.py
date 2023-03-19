import os
import datetime
import openai
from flask import Flask, redirect, render_template, request, url_for, make_response
import firebase_admin
from firebase_admin import credentials, firestore
from hierarchical_prompt import Storyteller

cred = credentials.Certificate("./gptstoryteller-firebase-adminsdk-bhz08-8514eb1c53.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

db = firestore.client()
collection = db.collection('messages')
CAST_FOLDER = "cast/"
app.config['CAST_FOLDER'] = CAST_FOLDER

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

def toChatCompletionMessages(messages):
    completionMessages = []
    for m in messages:
        completionMessages.append({"role" : "user" if m.sender == "USER" else "assistant", "content": m.text})
    return completionMessages

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

def createCASTInputs(background, uuid):
    outputDir = os.path.join(app.config['CAST_FOLDER'], "inputs/" + uuid)
    if os.path.exists(outputDir):
        os.system("rm -rf " + outputDir)
    os.mkdir(outputDir)
    messages = []
    with open("prompts/CAST_input_guide.txt", "r") as f:
        systemPrompt = f.read()
    userPrompt1 = "Based on the plot summary and character description, write interests.txt with at most 3 interests that are common among the characters. Do not include the filename."
    userPrompt1 += background
    messages.append({"role": "system", "content": systemPrompt})
    messages.append({"role": "user", "content": userPrompt1})
    interests = Storyteller().get_response(None, messages)
    with open(outputDir + "/interests.txt", "w") as f:
        f.write(interests)
    messages.append({"role": "assistant", "content": interests})
    userPrompt2 = "Do the same thing for facets.txt."
    messages.append({"role": "user", "content": userPrompt2})
    facets = Storyteller().get_response(None, messages)
    with open(outputDir + "/facets.txt", "w") as f:
        f.write(facets)
    messages.append({"role": "assistant", "content": facets})
    userPrompt3 = "Generate the instance.lp file by writing character() and level() rules for each interest and facet for each character. "
    messages.append({"role": "user", "content": userPrompt3})
    instance = Storyteller().get_response(None, messages, 1600)
    with open(outputDir + "/instance.lp", "w") as f:
        f.write(instance)
    messages.append({"role": "assistant", "content": instance})
    userPrompt4 = "Generate affinity rules for each interest with high-high, low-low, low-high, and high-low levels."
    messages.append({"role": "user", "content": userPrompt4})
    affinityByInterests = Storyteller().get_response(None, messages, 1600)
    messages.pop()
    userPrompt5 = "Generate affinity rules for each facet with high-high, low-low, low-high, and high-low levels."
    messages.append({"role": "user", "content": userPrompt5})
    affinityByFacets = Storyteller().get_response(None, messages, 1600)
    with open(outputDir + "/affinity_rules.lp", "w") as f:
        f.write(affinityByInterests + "\n" + affinityByFacets)
    #messages.append({"role": "assistant", "content": affinityByFacets})
    #messages.append({"role": "user", "content": userPrompt4})
    #messages.append({"role": "assistant", "content": affinityByInterests})
    #print(messages)

def getCASToutputs(uuid):
    cast_input_dir = os.path.join(app.config['CAST_FOLDER'], "inputs/" + uuid)
    if not os.path.exists(cast_input_dir):
        print("CAST Input Files Not Found.")
    from cast.clingo_file_formatter import run_clingo_formatter
    output_dir = os.path.join("outputs/" + uuid + '/')
    output_dir_cast = os.path.join(app.config['CAST_FOLDER'], "outputs/" + uuid + '/')
    if os.path.exists(output_dir_cast):
        os.system("rm -rf " + output_dir_cast)
    os.mkdir(output_dir_cast)
    run_clingo_formatter(cast_input_dir, output_dir_cast)
    os.chdir(output_dir_cast + "generated")
    os.system("clingo 1 * > ../" + "cast_output.txt")
    os.chdir("../../../../")
    from oracle import parse_cast_output
    parse_cast_output(output_dir_cast + "cast_output.txt", output_dir_cast + "parsed_output.txt")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
    #createCASTInputs("Summary: Walter Blue, an underpaid, overqualified, and dispirited high-school chemistry teacher who is struggling with a recent diagnosis of stage-three lung cancer. Blue turns to a life of crime and partners with a former student, Jesse Redman, to produce and distribute methamphetamine to secure his family\'s financial future before he dies, while navigating the dangers of the criminal underworld.\nCharacters Description: {\'Walter Blue (a.k.a. Heisenberg)\': \'Walter Blue is the main protagonist of the series. He is a high-school chemistry teacher who is diagnosed with lung cancer and turns to a life of crime as a way to ensure his family\\\'s financial future after his death. As he becomes increasingly involved in the criminal underworld, he adopts the alter-ego \"Heisenberg\" and becomes a ruthless drug kingpin.\', \'Jesse Redman\': \'Jesse Redman is a former student of Walter Blue and becomes his partner in the methamphetamine business. Initially, he is a reckless and immature drug dealer, but he becomes more responsible and empathetic as the series progresses.\', \'Skyler Blue\': \"Skyler Blue is Walter\'s wife and the mother of his two children. She initially disapproves of Walter\'s criminal activities but eventually becomes involved in his money laundering operation.\", \'Hank Schrader\': \'Hank Schrader is Walter\\\'s brother-in-law and a DEA agent who is investigating the methamphetamine trade in Albuquerque. He is initially unaware of Walter\\\'s involvement in the criminal underworld but eventually becomes obsessed with catching \"Heisenberg.\"\', \'Gustavo Fring\': \"Gustavo Fring is a drug lord and rival of Walter and Jesse\'s. He is a successful businessman who operates a chain of fast-food restaurants as a front for his drug empire.\", \'Saul Goodman\': \"Saul Goodman is a sleazy criminal lawyer who becomes Walter and Jesse\'s legal advisor. He is known for his colorful suits, cheesy advertisements, and unscrupulous tactics.\"}", "7ddae51d-171c-cb15-95f0-5d33b09f597a")