import openai
import os
import re
import backoff
import datetime
from tqdm import tqdm

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Message:
    def  __init__(self, sender, text, timestamp):
        self.sender = sender
        self.text = text
        self.timestamp = timestamp

class Storyteller:

    def  __init__(self):
        self.messages = []

    @backoff.on_exception(backoff.expo, (openai.error.RateLimitError, openai.error.APIConnectionError))
    def get_response_with_retry(self, prompt, messages=None, max_tokens=600, model="gpt-4"):
        if messages is not None:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.8,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
        else:
            response = openai.ChatCompletion.create(
                    model=model,
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

    def get_characters_desc(self, background):
        with open("prompts/char_prompt.txt", "r") as f:
            prompt = f.readline()
        prompt += background
        char_desc = self.get_response_with_retry(prompt)
        characters = re.findall("<character>(.*?)</character>", char_desc, re.DOTALL)
        descriptions = re.findall("<description>(.*?)</description>", char_desc, re.DOTALL)
        char_desc = {}
        for i in range(len(characters)):
            char_desc.update({characters[i]:descriptions[i]})
        return char_desc, descriptions


    def get_outlines(self, all_char_desc, background):
        char_desc_text = " ".join(all_char_desc)
        with open("prompts/outline_prompt.txt", "r") as f:
            prompt = f.readline()
        prompt = prompt + background + ' ' + char_desc_text + ' <scenes> '
        outline_text = self.get_response_with_retry(prompt, max_tokens=800)
        places = re.findall("<place>(.*?)</place>", outline_text, re.DOTALL)
        plot_ele = re.findall("<element>(.*?)</element>", outline_text, re.DOTALL)
        beats = re.findall("<beat>(.*?)</beat>", outline_text, re.DOTALL)
        outlines = []
        for i in range(len(places)):
            outlines.append((places[i], plot_ele[i], beats[i]))
        
        loc_names = list(set(places))
        return outlines, loc_names



    def get_location_desc(self, loc_names, background):
        loc_desc = {}
        with open("prompts/place_prompt_2.txt", "r") as f:
            prompt = f.readline()
        prompt = prompt + background + ' '
        for loc_name in tqdm(loc_names):
            prompt_loc = prompt + "<place>" + loc_name + "</place> " + "Description: "
            desc = self.get_response_with_retry(prompt_loc) #, model="gpt-3.5-turbo")
            loc_desc.update({loc_name: desc})

        with open("example_stories/loc_desc.txt", "w") as f:
            f.write(str(loc_desc))
        
        return loc_desc


    def get_stories(self, outlines, background, all_char_desc, loc_desc):
        previous_beats = ""
        stories = ""
        char_desc_text = " ".join(all_char_desc)
        prompt = "Imagine yourself as an intelligent storyteller. Based on the Background, Characters Descriptions, Place Description, Plot Element, and Story so far, elaborate the Next Beat into one paragraph. \n"
        prompt += "Background: " + background + "\n"
        self.messages.append(Message("Story Background", background, datetime.datetime.now()))
        prompt += "Characters Description: " + char_desc_text + "\n"
        self.messages.append(Message("Character Descriptions", char_desc_text, datetime.datetime.now()))
        for outline in tqdm(outlines):
            prompt_i = prompt
            prompt_i += "Place Description: " + loc_desc[outline[0]] + "\n"
            prompt_i += "Plot Element: " + outline[1] + "\n"
            # prompt_i += "Previous Beats: " + previous_beats + "\n"
            prompt_i += "Story so far: " + stories + "\n"
            prompt_i += "Next Beat: " + outline[2] + "\n"
            prompt_i += "Elaborated Paragraph: "
            previous_beats += outline[2] + "\n"
            story = self.get_response_with_retry(prompt_i) #, model="gpt-3.5-turbo")
            stories += story + "\n"
            self.messages.append(Message("Place: " + outline[0], loc_desc[outline[0]], datetime.datetime.now()))
            self.messages.append(Message("Beat - " + outline[1], outline[2], datetime.datetime.now()))
            self.messages.append(Message("Story - " + outline[1], story, datetime.datetime.now()))
        with open("example_stories/story.txt", "w") as f:
            f.write(stories)
        return self.messages

    def generate_story(self, background):
        # get characters descriptions from bg
        print("Generating characters...")
        char_desc, all_descriptions = self.get_characters_desc(background)
        # get chapters outlines from bg and characters desc
        print("Generating plot outlines...")
        outlines, loc_names = self.get_outlines(all_descriptions, background)
        # get location desc from location names and bg
        print("Generating location descriptions...")
        loc_desc = self.get_location_desc(loc_names, background)
        # get stories for each chapter with outlines
        print("Generating stories...")
        stories = self.get_stories(outlines, background, char_desc, loc_desc)
        
        return stories
    

    # zero-short hierarchical prompt
    def get_char_desc_zero_shot(self, background, uuid, use_cast=True, zero_shot=True):
        if zero_shot is False:
            with open("prompts/char_prompt.txt", "r") as f:
                prompt = f.readline() + "\n"
        else:
            prompt = ""
        prompt += "Based on the following Background, generate a list of characters with descriptions about their roles in the story. Consider what they might do and the goals they might have based on the Character relations. Each character has its name wrapped in <character>[name]</character>, and its description in <description>[character description]</description>: \nBackground: "
        prompt += background
        if use_cast:
            with open(os.path.join("cast/", "outputs/" + uuid + '/parsed_output.txt'), "r") as f:
                cast_relations = f.read()
            prompt += "Character Relations: " + cast_relations
        char_desc = self.get_response_with_retry(prompt, max_tokens=800)
        characters = re.findall("<character>(.*?)</character>", char_desc, re.DOTALL)
        descriptions = re.findall("<description>(.*?)</description>", char_desc, re.DOTALL)
        char_desc = {}
        all_char_desc = []
        for i in range(len(characters)):
            char_desc.update({characters[i]:descriptions[i]})
            all_char_desc.append(characters[i] + ": " + descriptions[i])
        with open("example_stories/char_desc.txt", "w") as f:
            f.write(str(char_desc))
        return char_desc, all_char_desc

    def get_outline_zero_shot(self, background, all_char_desc, uuid, use_cast=True, zero_shot=True):
        char_desc_text = " ".join(all_char_desc)
        if zero_shot is False:
            with open("prompts/outline_prompt.txt", "r") as f:
                prompt = f.readline()
        else:
            prompt = ""
        prompt += "Based on Background, Character Descriptions, and Character Relations. Fill the [location name] with location names and [beat] with a 2-4 sentences story beats in each plot element. \n"
        prompt += "Background: " + background + "\n"
        prompt += "Character Descriptions: " + char_desc_text + "\n"
        if use_cast:
            with open(os.path.join("cast/", "outputs/" + uuid + '/parsed_output.txt'), "r") as f:
                cast_relations = f.read()
            prompt += "Character Relations: " + cast_relations + "\n"
        with open("prompts/template_pyramid.txt", "r") as f:
            template = f.read()
        prompt += template
        outline_text = self.get_response_with_retry(prompt, max_tokens=800)
        places = re.findall("<place>(.*?)</place>", outline_text, re.DOTALL)
        plot_ele = re.findall("<element>(.*?)</element>", outline_text, re.DOTALL)
        beats = re.findall("<beat>(.*?)</beat>", outline_text, re.DOTALL)
        outlines = []
        for i in range(len(places)):
            outlines.append((places[i], plot_ele[i], beats[i]))
        
        loc_names = list(set(places))
        with open("example_stories/outlines.txt", "w") as f:
            f.write(str(outlines))
        return outlines, loc_names

    def generate_story_cast(self, background, uuid):
        print("Modifying character descriptions...")
        _, all_desc = self.get_char_desc_zero_shot(background, uuid)
        print("Generating story outlines...")
        outlines, loc_names = self.get_outline_zero_shot(background, all_desc, uuid)
        print("Generating location descriptions...")
        loc_desc = self.get_location_desc(loc_names, background)
        print("Writing the whole story...")
        stories = self.get_stories(outlines, background, all_desc, loc_desc)
        return stories

if __name__ == "__main__":
    background = "Walter Blue, an underpaid, overqualified, and dispirited high-school chemistry teacher who is struggling with a recent diagnosis of stage-three lung cancer. Blue turns to a life of crime and partners with a former student, Jesse Redman, to produce and distribute methamphetamine to secure his family's financial future before he dies, while navigating the dangers of the criminal underworld."
    # story = Storyteller().generate_story("Walter Blue, an underpaid, overqualified, and dispirited high-school chemistry teacher who is struggling with a recent diagnosis of stage-three lung cancer. Blue turns to a life of crime and partners with a former student, Jesse Redman, to produce and distribute methamphetamine to secure his family's financial future before he dies, while navigating the dangers of the criminal underworld.")
    # print(story)
    storyteller = Storyteller()
    #char_desc, all_char_desc = storyteller.get_char_desc_zero_shot(background, "7ddae51d-171c-cb15-95f0-5d33b09f597a")
    #storyteller.get_outline_zero_shot(background, char_desc, "7ddae51d-171c-cb15-95f0-5d33b09f597a")
    story = storyteller.generate_story_cast(background, "7ddae51d-171c-cb15-95f0-5d33b09f597a")
