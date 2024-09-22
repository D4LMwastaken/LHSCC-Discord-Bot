# Main.py
"""
    Version 2.9 of the Python Discord Bot programmed by D4LM.
    The purpose of this bot is to be a simple Discord Bot that can communicate with users.
"""
# Import all the necessary modules.
# Discord.py is a Python library used to interact with the Discord API.
# It is used to create the Discord Bot.
import discord  # Website: https://guide.pycord.dev/installation

# The OS module is a built-in Python module that provides a way to use the operating
# system dependent functionality.
# It is used to get the .env file.
import os  # Built in Python module. Used to get the .env file.

# The random module is a built-in Python module that implements pseudo-random number
# generators for various distributions.
# It is used to add randomness to the Discord Bot.
import random  # Built in Python module. Allows me to use randomness in my Discord Bot.

# The load_dotenv() function is a Python function from the python-dotenv package.
# It is used to load the .env file.
from dotenv import load_dotenv  # Python package. Used to load the .env file.

# Get the environment variables from the .env file.
load_dotenv()

# Get the Discord Bot Token from the .env file.
Discord_Bot_Token = os.getenv('DISCORD_BOT_TOKEN')

# Create the Discord Bot.
Discord_Bot = discord.Bot()

# About the project variables
Version = "2.9"  # Note: Change a version every time you make modifications to code. Merged developer and
# release editions into one.
DateUpdated = "9/22/2024"  # Change the release date into the last time you updated.
Language = "Python"  # Change the language only if the code is in a different version or variant.
Dev = "D4LM"  # Change if you are the one who creates a fork of this project.
CoDev = "None is the apprentice yet..."  # This is a place to put maintainers of your project.
UpdatedItems = ("The last version before 3.0!" + "\n" + "Changed package from Discord.py to pycord "
                                                        "Split the bot into two, a master & an apprentice!")

# Lists the Discord Bot uses
# Greetings is a list of strings that are used to greet users.
# goodbyes is a list of strings that are used to say goodbye to users.
# commands is a list of strings that are used to store all the commands the bot has.
greetings = ["Hello!", "What's up!", "Howdy!", "Greetings!"]
goodbyes = ["Bye!", "Goodbye!", "See you later!", "See you soon!"]
commands = ["/Music", "/Pet", "/Book", "/Video Games", "/PING", "/Job", "/About Me", "/Bye", "/Help", "/Version",
            "/New Stuff", "/Self Destruct", "/Gemini"]  # Put new commands here.


# Required functions
def random_list_item(chosen_list):
    """
    The necessary function required.
    Used to make sure the chosen elements in the list are random.
    If used inside @Client.event, it will stop certain replies from being random.
    """
    chosen_number = random.randrange(0, len(chosen_list))
    chosen_item = chosen_list[chosen_number]
    return chosen_item


@Discord_Bot.event
async def on_ready():
    """
    Called when the bot is ready. Prints a message to the console to indicate that the bot is online and ready.
    """
    print(f"{Discord_Bot.user} is ready & online!")


@Discord_Bot.event
async def on_connect():  # Syncs the new commands to the Discord Server
    if Discord_Bot.auto_sync_commands:
        await Discord_Bot.sync_commands()
        print("All commands synced!")


cogs_list = [  # List of cogs to load
    'Keywords_And_Responses',
    'Math',
    'Gemini'
]

for cog in cogs_list:  # Load the cogs into the Discord Bot
    Discord_Bot.load_extension(f'cogs.{cog}')


@Discord_Bot.slash_command(name="ping", description="Ping the bot to send Pong!")
async def ping(ctx: discord.ApplicationContext):
    """
    This is the ping command. It checks the latency of the Discord Bot and sends it to the user as "Pong! <latency>".
    """
    await ctx.respond(f"Pong! Latency is {Discord_Bot.latency}")


@Discord_Bot.slash_command(name="hi", description="Sends a greeting to the user.")
async def hi(ctx: discord.ApplicationContext):
    """
    Sends a greeting to the user.

    This function sends a random greeting from the list called greetings.
    """
    await ctx.respond(random_list_item(greetings))


@Discord_Bot.slash_command(name="help", description="Sends out all the possible commands for the bot.")
async def help(ctx: discord.ApplicationContext):
    """
    Sends out all the possible commands for the bot.
    """
    await ctx.respond(" ".join(commands))


@Discord_Bot.slash_command(name="bye", description="Says a goodbye to the bot.")
async def bye(ctx: discord.ApplicationContext):
    """
    Says a goodbye to the bot.

    This function sends a random goodbye from the list called goodbyes.
    """
    await ctx.respond(random_list_item(goodbyes))
    print(random_list_item(goodbyes))
    print("This is not an error! Bot closed by command!")
    exit()


"""
    Note: Remember to make this code only work for user with certain permission in Discord server settings.
    Another Note: There is no exit code since the bot is leaving as the user intended.
"""


@Discord_Bot.slash_command(name="version", description="Gives version information to the usear about the Discord Bot.")
async def version(ctx: discord.ApplicationContext):
    """
    Gives version information to the user about the Discord Bot.

    This function sends a message to the user telling the user the version of the bot, the date it was last updated,
    the programming language it was written in, the developer of the bot, and the assistant developer/maintainer.

    :param ctx: The context of the command.
    :type ctx: discord.ApplicationContext
    """
    await ctx.respond("Version: " + Version + "\n" + "Date Updated: " + DateUpdated + "\n" + "Language: " + Language +
                      "\n" + "Developer: " + Dev + "\n" + "Assistant Developer/maintainer: " + CoDev)


@Discord_Bot.slash_command(name="new_stuff", description="Shows what is new to the bot.")
async def new_stuff(ctx: discord.ApplicationContext):
    """
    Shows what is new to the bot.

    This function sends a message to the user telling the user what is new with the bot in the current version.

    :param ctx: The context of the command.
    :type ctx: discord.ApplicationContext
    """
    # Get the changelog for the version.
    changelog = UpdatedItems

    # Send the changelog to the user.
    await ctx.respond("For version " + Version + ".\nHere is the Changelog: " + changelog)


@Discord_Bot.slash_command(name="self_destruct", description="Self-destructs the bot.")
async def self_destruct(ctx: discord.ApplicationContext):
    """
    Self-destructs the bot.

    This function sends a countdown message to the user and then sends a message telling the user the bot has exploded.
    Then it will exit the program.

    :param ctx: The context of the command.
    :type ctx: discord.ApplicationContext
    """
    # Send a message to the user to prepare for the countdown.
    await ctx.respond("Preparing to blow up...")

    # Start the countdown.
    await ctx.respond('3')
    await ctx.respond('2')
    await ctx.respond('1')

    # Send a message to the user that the bot is going to explode.
    await ctx.respond("BOOM!")

    # Log to the console that the bot has exploded.
    print("Discord Bot exploded!")

    # Exit the program.
    exit()


# The last line of the code is to run the bot with the token
# found in the .env file.
# The token is used to authenticate the bot with the Discord servers.
# The bot will not be able to connect to the Discord servers if the token is invalid.
# The bot will also not be able to connect to the Discord servers if the bot is not enabled.
# The bot will also not be able to connect to the Discord servers if the bot is not verified.
"""
    This is the last line of code.
    It runs the bot with the token found in the .env file.
    The token is used to authenticate the bot with the Discord servers.
    The bot will not be able to connect to the Discord servers if the token is invalid.
    The bot will also not be able to connect to the Discord servers if the bot is not enabled.
    The bot will also not be able to connect to the Discord servers if the bot is not verified.
"""
Discord_Bot.run(Discord_Bot_Token)
