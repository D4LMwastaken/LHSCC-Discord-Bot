import os
import discord
from discord.ext import commands
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)


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


class Gemini(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    gemini = discord.SlashCommandGroup("gemini", "Commands for the Gemini AI")

    @gemini.command(name="ask", description="Ask Gemini a question")
    async def ask_gemini(self, ctx, question: str):
        await ctx.respond(genai_question(question))

    @gemini.command(name="ask_pro", description="Ask Gemini Pro Model a question")
    async def ask_gemini_pro(self, ctx, question: str):
        await ctx.respond(genai_question_pro(question))


def setup(bot):
    bot.add_cog(Gemini(bot))
