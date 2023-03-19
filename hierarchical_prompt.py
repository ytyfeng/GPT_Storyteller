import openai
import os
import re

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Storyteller:

    def get_response(self, prompt, messages=None, max_tokens=600):
        if messages is not None:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.8,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
        else:
            response = openai.ChatCompletion.create(
                    model="gpt-4",
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
        char_desc = self.get_response(prompt)
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
        outline_text = self.get_response(prompt, max_tokens=800)
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
        with open("prompts/place_prompt.txt", "r") as f:
            prompt = f.readline()
        prompt = prompt + background + ' '
        for loc_name in loc_names:
            prompt_loc = prompt + "<place>" + loc_name + "</place> " + "Description: "
            desc = self.get_response(prompt_loc)
            loc_desc.update({loc_name: desc})
        
        return loc_desc


    def get_stories(self, outlines, background, char_desc, loc_desc):
        stories = ""
        print("Summary: " + background)
        print("Characters Description: " + str(char_desc))
        for outline in outlines:
            print("Place: " + outline[0])
            print("Place Description: " + loc_desc[outline[0]])
            print("Plot Element: " + outline[1])
            print("Beat: " + outline[2])
        
        return stories

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
    def get_char_desc_zero_shot(self, background, uuid, use_cast=True):
        prompt = "based on the Background and Character Relations, generate a list of characters with descriptions about their roles in the story. Consider what they might do and the goals they might have based on their relations. Each character has its name wrapped in <character>[name]</character>, and its description in <description>[character description]</description>: \nBackground: "
        prompt += background
        if use_cast:
            with open(os.path.join("cast/", "outputs/" + uuid + '/parsed_output.txt'), "r") as f:
                cast_relations = f.read()
            prompt += "Character Relations: " + cast_relations
        char_desc = self.get_response(prompt)
        characters = re.findall("<character>(.*?)</character>", char_desc, re.DOTALL)
        descriptions = re.findall("<description>(.*?)</description>", char_desc, re.DOTALL)
        char_desc = {}
        for i in range(len(characters)):
            char_desc.update({characters[i]:descriptions[i]})
        with open("example_stories/char_desc.txt", "w") as f:
            f.write(str(char_desc))
        return char_desc, descriptions

    def get_outline_zero_shot(self, background, all_char_desc, uuid, use_cast=True):
        char_desc_text = " ".join(all_char_desc)
        prompt = "Based on Background, Character Descriptions, and Character Relations. Fill the [location name] and [beat] with location names and story beats in each plot element. \n"
        prompt += "Background: " + background + "\n"
        prompt += "Character Descriptions: " + char_desc_text + "\n"
        if use_cast:
            with open(os.path.join("cast/", "outputs/" + uuid + '/parsed_output.txt'), "r") as f:
                cast_relations = f.read()
            prompt += "Character Relations: " + cast_relations + "\n"
        with open("prompts/template_pyramid.txt", "r") as f:
            template = f.read()
        prompt += template
        outline_text = self.get_response(prompt, max_tokens=800)
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

    def get_location_desc_zero_shot():
        pass
    

if __name__ == "__main__":
    background = "Walter Blue, an underpaid, overqualified, and dispirited high-school chemistry teacher who is struggling with a recent diagnosis of stage-three lung cancer. Blue turns to a life of crime and partners with a former student, Jesse Redman, to produce and distribute methamphetamine to secure his family's financial future before he dies, while navigating the dangers of the criminal underworld."
    # story = Storyteller().generate_story("Walter Blue, an underpaid, overqualified, and dispirited high-school chemistry teacher who is struggling with a recent diagnosis of stage-three lung cancer. Blue turns to a life of crime and partners with a former student, Jesse Redman, to produce and distribute methamphetamine to secure his family's financial future before he dies, while navigating the dangers of the criminal underworld.")
    # print(story)
    storyteller = Storyteller()
    char_desc, all_char_desc = storyteller.get_char_desc_zero_shot(background, "7ddae51d-171c-cb15-95f0-5d33b09f597a")
    storyteller.get_outline_zero_shot(background, char_desc, "7ddae51d-171c-cb15-95f0-5d33b09f597a")