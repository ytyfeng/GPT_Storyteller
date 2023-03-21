# GPT Storyteller
### Ty Feng, Wenchang Liu, Frank Gomez

This is the GPT Storyteller web app. It uses the [Flask](https://flask.palletsprojects.com/en/2.0.x/) web framework. 

## Live Demo

Instead of setting up the project yourself, you can also find our live demo at [http://gpt-story.com](http://gpt-story.com).

## Setup

1. Clone this repository.

3. Navigate into the project directory:

   ```bash
   $ cd GPT_Storyteller
   ```

4. Create a new virtual environment:

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```
   Install clingo for CAST:

   ```bash
   $ sudo apt install gringo
   ````
   To set up Firebase for the FireStore DB used in the project:

   ```bash
   $ pip install firebase-admin
   ```

   Download your private key for the Firebase Admin SDK from [https://console.firebase.google.com/u/0/project/gptstoryteller/settings/serviceaccounts/adminsdk](https://console.firebase.google.com/project/gptstoryteller/settings/serviceaccounts/adminsdk). Move the private key to this project's directory. Make sure this line `cred = credentials.Certificate()` in [app.py](app.py) has the correct private key path. 

6. Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

7. Add your [OpenAI API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.
   If your API key does not have access to GPT-4, change line 24 in [hierarchical_prompt.py](hierarchical_prompt.py) to use "gpt-3.5-turbo" instead.

8. Run the app:

   ```bash
   $ python app.py
   ```

You should now be able to access the app at [http://localhost](http://localhost)!
