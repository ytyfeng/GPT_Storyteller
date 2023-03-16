import openai
openai.api_key = ""
import re


def get_response(prompt, max_tokens=600):
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.8,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
    return response.choices[0].message.content


def get_characters_desc(background):
    with open("prompts/char_prompt.txt", "r") as f:
        prompt = f.readline()
    prompt += background
    char_desc = get_response(prompt)
    characters = re.findall("<character>(.*?)</character>", char_desc, re.DOTALL)
    descriptions = re.findall("<description>(.*?)</description>", char_desc, re.DOTALL)
    char_desc = {}
    for i in range(len(characters)):
        char_desc.update({characters[i]:descriptions[i]})
    return char_desc, descriptions


def get_outlines(all_char_desc, background):
    char_desc_text = " ".join(all_char_desc)
    with open("prompts/outline_prompt.txt", "r") as f:
        prompt = f.readline()
    prompt = prompt + background + ' ' + char_desc_text + ' <scenes> '
    outline_text = get_response(prompt, max_tokens=800)
    # if outline_text[-7:] != "</beat>":
    #     outline_text += "</beat>"
    print(outline_text)
    places = re.findall("<place>(.*?)</place>", outline_text, re.DOTALL)
    plot_ele = re.findall("<element>(.*?)</element>", outline_text, re.DOTALL)
    beats = re.findall("<beat>(.*?)</beat>", outline_text, re.DOTALL)
    outlines = []
    for i in range(len(places)):
        outlines.append((places[i], plot_ele[i], beats[i]))
    
    loc_names = list(set(places))
    return outlines, loc_names


def get_location_desc(loc_names, background):
    loc_desc = {}
    with open("prompts/place_prompt.txt", "r") as f:
        prompt = f.readline()
    prompt = prompt + background + ' '
    for loc_name in loc_names:
        prompt_loc = prompt + "<place>" + loc_name + "</place> " + "Description: "
        desc = get_response(prompt_loc)
        loc_desc.update({loc_name: desc})
    
    return loc_desc


def get_stories(outlines, background, char_desc, loc_desc):
    stories = ""
    print("Summary: " + background)
    print("Characters Description: " + str(char_desc))
    for outline in outlines:
        print("Place: " + outline[0])
        print("Place Description: " + loc_desc[outline[0]])
        print("Plot Element: " + outline[1])
        print("Beat: " + outline[2])
    
    return stories

def generate_story(background):
    # get characters descriptions from bg
    print("Generating characters...")
    char_desc, all_descriptions = get_characters_desc(background)
    # get chapters outlines from bg and characters desc
    print("Generating plot outlines...")
    outlines, loc_names = get_outlines(all_descriptions, background)
    # get location desc from location names and bg
    print("Generating location descriptions...")
    loc_desc = get_location_desc(loc_names, background)
    # get stories for each chapter with outlines
    print("Generating stories...")
    stories = get_stories(outlines, background, char_desc, loc_desc)
    
    return stories

generate_story("Walter Blue, an underpaid, overqualified, and dispirited high-school chemistry teacher who is struggling with a recent diagnosis of stage-three lung cancer. Blue turns to a life of crime and partners with a former student, Jesse Redman, to produce and distribute methamphetamine to secure his family's financial future before he dies, while navigating the dangers of the criminal underworld.")