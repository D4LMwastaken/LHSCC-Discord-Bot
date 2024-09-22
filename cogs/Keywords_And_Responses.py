# Keywords_And_Responses.py
# Keywords_And_Responses.py
"""
    This cog contains the commands for the user to learn more about the bot.
    The bot will respond with a message containing information about it.
"""

# Import the necessary modules
import discord
from discord.ext import commands

"""
    Import the necessary modules.

    discord: The official Discord API library for Python.
    discord.ext.commands: A framework for creating commands for the Discord API.
"""

"""
    List of keywords that the bot will respond to.

    This list contains the commands that the bot will respond to.
    It is recommended to add a comma after each item, making sure the item is enclosed in quotation marks.
    The two lists, keywords and responses work by when a Discord user sends a message with one of the items in the
        keywords list, the keywords list being indexed from 0 to the last item (!Music=0, !Pet =1, etc.). Then it will 
        take the index location of that keyword and put it into the response list with the index being the index 
        location of the keyword. 
    Recommended if you want to make a basic command without having to make an if statement for each one.
"""
keywords = ["/Music", "/Pet", "/Book", "/Video Games", "/Ping", "/Job", "/About Me"]

"""
    List of responses to the keywords.

    This list contains the responses to the commands in the keywords list.
    It is recommended to add a comma after each item, making sure the item is enclosed in quotation marks.
    The two lists, keywords and responses work by when a Discord user sends a message with one of the items in the
        keywords list, the keywords list being indexed from 0 to the last item (!Music=0, !Pet =1, etc.). Then it will 
        take the index location of that keyword and put it into the response list with the index being the index 
        location of the keyword. 
    Recommended if you want to make a basic command without having to make an if statement for each one.
"""
responses = ["Music is so relaxing!", "Dogs are man's best friend!", "I know a lot of books.",
             "I like to play video games. My favorite are World of Warships, Minecraft, 0AD and Roblox.", "Pong!",
             "Help and advise the Largo High School Coding Club Discord server.",
             "A Discord bot made by D4LM who is smart and amazing."]


class Keywords_And_Responses(commands.Cog):
    def __init__(self, bot):
        """
        This is a special method that is called when the cog is loaded.

        :param bot: The bot instance.
        """
        self.bot = bot

    @discord.slash_command(name="music", description="Gives some information about the music.")
    async def music(self, ctx):
        """
        This function is a slash command that sends a message when the /music command is used.
        It sends a random item from the list of responses.
        """
        await ctx.respond(responses[0])

    @discord.slash_command(name="pet", description="Gives some information about the pets.")
    async def pet(self, ctx):
        """
        This function is a slash command that sends a message when the /pet command is used.
        It sends a random item from the list of responses.
        """
        await ctx.respond(responses[1])

    @discord.slash_command(name="book", description="Gives some information about the books.")
    async def book(self, ctx: discord.ApplicationContext):
        """
        This function is a slash command that sends a message when the /book command is used.
        It sends a random item from the list of responses.
        """
        await ctx.respond(responses[2])

    @discord.slash_command(name="video_games", description="Gives some information about the video games.")
    async def video_games(self, ctx):
        """
        This function is a slash command that sends a message when the /video_games command is used.
        It sends a random item from the list of responses.
        """
        # Send a random item from the list of responses when the /video_games command is used.
        await ctx.respond(responses[3])

    @discord.slash_command(name="job", description="Gives some information about the job.")
    async def job(self, ctx: discord.ApplicationContext):
        """
        This function is a slash command that sends a message when the /job command is used.
        It sends a random item from the list of responses.
        """
        # Send a random item from the list of responses when the /job command is used.
        await ctx.respond(responses[5])

    @discord.slash_command(name="about_me", description="Gives some information about me.")
    async def about_me(self, ctx):
        """
        This function is a slash command that sends a message when the /about_me command is used.
        It sends a random item from the list of responses.
        """
        # Send a random item from the list of responses when the /about_me command is used.
        await ctx.respond(responses[6])


def setup(bot):
    """
    This function is called when the cog is loaded.

    It adds the Keywords_And_Responses cog to the bot.
    """
    bot.add_cog(Keywords_And_Responses(bot))
