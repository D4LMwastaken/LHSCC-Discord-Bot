# DiscordBot2.7.py
"""
    Version 2.7 of the Python DiscordBot programmed by D4LM.
    Please read the README.md for installation, contact information, changelog, and installation.
"""
# Dependencies
import discord  # Website: https://discordpy.readthedocs.io/en/stable/
import os  # Built in Python module. Used to get the .env file.
import random  # Built in Python module. Allows me to use randomness in my Python Script.
import Gemini  # A function library attached to the DiscordBot2.7.py folder. Needed to use the !Ask Gemini command.

# .env file support
from dotenv import load_dotenv

load_dotenv()  # Get the environment variables from the .env you added.

# About the project variables
Version = "2.7"  # Note: Change version every time you make modifications to code. Merged developer and
# release editions into one.
DateUpdated = "8/25/2024"  # Change the release date into the last time you updated.
Language = "Python"  # Change the language only if the code is in a different version or variant.
Dev = "D4LM"  # Change if you are the one who creates a fork of this project.
CoDev = ""  # This is a place to put maintainers of your project.
UpdatedItems = ("Third version. " + "\n" + "Organized DiscordBot 2.7.py to be more clear. "
                                           "Added !Ask GeminiPro command.")

# Discord package required code
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Lists the Discord Bot uses
greetings = ["Hello!", "What's up!", "Howdy!", "Greetings!"]
goodbyes = ["Bye!", "Goodbye!", "See you later!", "See you soon!"]
commands = ["!Music", "!Pet", "!Book", "!Video Games", "!PING", "!Job", "!About Me", "!Bye", "!Help", "!Version",
            "!New Stuff", "!Self Destruct", "!Ask Gemini"]  # Put new commands here.
keywords = ["!Music", "!Pet", "!Book", "!Video Games", "!Ping", "!Job", "!About Me"]
responses = ["Music is so relaxing!", "Dogs are man's best friend!", "I know a lot of books.",
             "I like to play video games. My favorite are World of Warships, Minecraft, 0AD and Roblox.", "Pong!",
             "Help and advise the Largo High School Coding Club Discord server.",
             "A Discord bot made by D4LM who is smart and amazing."]
"""
    To add more items to the lists add a comma after hte item, making sure the item is enclosed in quotation marks.
    The two lists, keywords and responses work by when a Discord user sends a message with one of the items in the
        keywords list, the keywords list being indexed from 0 to the last item (!Music=0, !Pet =1, etc.). Then it will 
        take the index location of that keyword and put it into the response list with the index being the index 
        location of the keyword. 
    Recommended if you want to make a basic command without having to make an if statement for each one.
"""


# Required functions
def random_list_item(chosen_list):
    """
    Necessary function required.
    Used to make sure the chosen elements in the list are random.
    If used inside @Client.event, it will stop certain replies from being random.
    """
    chosen_number = random.randrange(0, len(chosen_list))
    chosen_item = chosen_list[chosen_number]
    return chosen_item


# Required. Starts DiscordBot code.
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    # Function that contacts Discord and gives what username/display name the bot is under.


# Rest of the coded for the Discord Bot
@client.event
async def on_message(message):
    if message.author == client.user:
        return
        # Required if statement. Stops the Discord Bot from replying to itself.

    if '!HI' in str.upper(message.content):
        await message.channel.send(random_list_item(greetings))
        # If a user sends '!HI' or similarly, the bot will say a random greeting.

    if '!HELP' in str.upper(message.content):
        # Send out all the possible commands for the Discord Bot.
        await message.channel.send(" ".join(commands))

    if '!BYE' in str.upper(message.content):
        """
            The user sends "!Bye" from Discord, telling the Discord Bot to go to rest.
            Note: Add code later to check weather the user has authorization to stop the bot or else the bot will have 
            to be restarted on the server.
            Another note: There is no exit code since the bot is leaving as the user intended.
        """
        await message.channel.send(random_list_item(goodbyes))
        print(random_list_item(goodbyes))
        exit()

    if '!VERSION' in str.upper(message.content):
        # Command that gives version information to the user about the discord bot.
        await message.channel.send('Version: ' + Version + '\n' + 'Date Updated: ' + DateUpdated + '\n' + 'Language: ' +
                                   Language + '\n' + 'Developer: ' + Dev + '\n' + 'Assistant Developer/maintainer: ' +
                                   CoDev)

    if '!NEW STUFF' in str.upper(message.content):
        # Command that gives what code was modified.
        await message.channel.send('For Version ' + Version + '. These stuff were added: ' + '\n' + UpdatedItems)

    if '!SELF DESTRUCT' in str.upper(message.content):
        """
            Dp not remove the message.channel.send repeats and use \n, this is for dramatic effect.
            Note: Add a statement to check if the user is authorized to use this command.
        """
        await message.channel.send('Preparing to blow up...')
        await message.channel.send('3')
        await message.channel.send('2')
        await message.channel.send('1')
        await message.channel.send('Boom!')
        exit()

    if '!ASK GEMINI' in str.upper(message.content):
        # New command that the user could use to ask a question to a Gemini AI bot.
        await message.channel.send('What do you want to ask? Please do not ask for something more than 2000 '
                                   'characters.')
        reply = await client.wait_for("message")
        if "!PRO" in str.upper(reply.content):
            await message.channel.send(
                'What do you want to ask for the pro version? Please do not ask a question that will'
                ' generate more than 2000 characters.')
            reply = await client.wait_for("message")
            answer = Gemini.genai_question_pro(reply.content)
            await message.channel.send(answer)
        else:
            answer = Gemini.genai_question(reply.content)
            await message.channel.send(answer)

    for index, keyword in enumerate(keywords):
        """
            For statement that checks if the keywords in the keyword list match in the user message, if it does, 
            it sends the correct response.
        """
        if str.upper(keyword) in str.upper(message.content):
            await message.channel.send(responses[index])


client.run(os.getenv('DISCORD_BOT_KEY'))
"""
    Empty by default when install.
    Steps to fix:
        1. Go to https://discord.com/developers and get your key.
        2. Create an environmental variable with the name "Discord_BOT_KEY" and the value being your key. Please don't 
        surround the value with quotes.
"""
