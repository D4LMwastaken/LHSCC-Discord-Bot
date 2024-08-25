import os  # Built in module in Python that is necessary to get the .env file.

import google.generativeai as genai  # Import the necessary module that the

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# !Ask Gemini command and this function library to work. Website: https://ai.google.dev/gemini-api
# Install Website: https://ai.google.dev/gemini-api/docs/quickstart?lang=python

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # Environmental variable that you should have got from Google AI Studio.

genai.configure(api_key=GOOGLE_API_KEY)  # Tells the module which one of your variables is the Google AI Keu


def genai_question(question):  # Function used in the main script
    model = genai.GenerativeModel('gemini-1.5-flash')  # Model that the !Ask Gemini uses.
    response = model.generate_content("In less than 2000 characters." + question)  # The "In less than 2000 characters"
    # just tells the bot to not type more than 2000 characters.
    print(response)
    if response == "":  # Tells why the message could not be sent
        print("Unable to receive message, check message to make sure it is safe or not...")
        return "Unable to receive message, check message to make sure it is safe or not..."
    elif len(response.text) >= 2000:  # Creates an else if statement to check also if the text is too long to be sent
        # by Discord
        print("text too long")
        return "The text is too long to be sent, try another answer that takes up less text."
    else:
        print(response.text)
        return response.text


def genai_question_pro(question):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content("In less than 2000 characters." + question)
    # just tells the bot to not type more than 2000 characters.
    print(response)
    if response == "":  # Tells why the message could not be sent
        print("Unable to receive message, check message to make sure it is safe or not...")
        return "Unable to receive message, check message to make sure it is safe or not..."
    elif len(response.text) >= 2000:  # Creates an else if statement to check also if the text is too long to be sent
        # by Discord
        print("text too long")
        return "The text is too long to be sent, try another answer that takes up less text."
    else:
        print(response.text)
        return response.text
