# Dependencies
import discord  # Instructions to install/website: https://discordpy.readthedocs.io/en/stable/
import os  # Built in module in Python that is needed to get the .env file.
import random  # Built-in Python module that allows some items, like greetings and goodbyes, to be random.
import Gemini  # A function library attached to the project file that is labeled "Gemini.py".
# This function library is necessary to make the !Ask Gemini command work.
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

# DiscordBot2.6.py
"""
    Version 2.6 of the Python Discord Bot coded by D4LM
    Please read the ReadMe.MD for installation, issues, changelog and other information about this Python file.
"""
Version = "2.6 (Developer Edition)"
"""
    Note: Change version every time you make modifications to the code. Change the 
    edition if you are using for testing/developing purposes (Developer Edition) or are running a stable file for the 
    server-side (Release Edition) 
"""
DateUpdated = "7/21/2024"  # Change the release date to the last time you made modifications to the code
Language = "Python"  # Change the language only if your transcode it into another language.
Dev = "D4LM"  # Change the developer only if you modified the code at least 50%.
CoDev = ""  # For maintainers or people who helped code at least 5% of this Python file.
UpdatedItems = ("Second version. " + "\n" + "This version added a built-io 2000 character limit for Gemini AI. Will "
                                            "not exceed 2000 character limit unless you tell it to do so.")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Lists for the Discord Bot (General)
greetings = ["Hello!", "What's up!", "Howdy!", "Greetings!"]  # List of greetings to use.
goodbyes = ["Bye!", "Goodbye!", "See you later!", "See you soon!"]  # List of goodbyes to use.
commands = ["!Music", "!Pet", "!Book", "!Video Games", "!PING", "!Job", "!About Me", "!Bye", "!Help", "!Version",
            "!New Stuff", "!Self Destruct", "!Ask Gemini"]  # Put new commands here

# Keywords and responses lists
keywords = ["!Music", "!Pet", "!Book", "!Video Games", "!Ping", "!Job", "!About Me"]
responses = ["Music is so relaxing!", "Dogs are man's best friend!", "I know a lot of books.",
             "I like to play video games. My favorite are World of Warships, Minecraft, 0AD and Roblox.", "Pong!",
             "Help and advise the Largo High School Coding Club Discord server.",
             "A Discord bot made by D4LM who is smart and amazing."]
"""
    To add more items ot the lists add a comma after the item, making sure the item is enclosed in quotation marks.
    The two arrays work by saying for instance, "!Music", it will reply typing "Music is so relaxing".
    Recommended for coders to use to make it easier to add commands are very short and simple like !PING.
"""


# Functions
def random_list_item(chosen_list):
    """
        Necessary function required to make sure the chosen elements in the list are random.
        If this function is used inside client event it will only work once and stop being random.
    """
    chosen_integer = random.randrange(0, len(chosen_list)) 
    chosen_element = chosen_list[chosen_integer]
    return chosen_element


@client.event
async def on_ready():
    # Test statement to tell the developer and make sure that the bot went into the Discord Server and went under
    # what username/display name.
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        # Stops the Discord Bot from replying to itself.
        return

    if '!HI' in str.upper(message.content):
        # If user sends '!HI' or similar, the bot will say a random greeting.
        await message.channel.send(random_list_item(greetings))

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
