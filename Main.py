"""
Main bot file that handles initialization, commands, and event listeners.
This file serves as the entry point for the Discord bot and manages core functionality.
"""

import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import asyncio
import random
from cogs.Gemini import gemini_generate

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# List of guild IDs where the bot will be active
GUILD_IDS = [
    1228003403171627078,
    1239233526835056781
]

class Bot(commands.Bot):
    """
    Main bot class that inherits from commands.Bot.
    Handles initialization of cogs and core bot functionality.
    """
    def __init__(self):
        # Initialize bot with command prefix and all intents enabled
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        # List of cogs to be loaded on startup
        self.initial_extensions = [
            'cogs.KeywordsAndResponses',
            'cogs.Math',
            'cogs.Gemini',
            'cogs.Calendar',
            'cogs.Physics'
        ]

    async def setup_hook(self):
        """
        Loads all cogs during bot startup.
        Prints success/error messages for each cog loading attempt.
        """
        for ext in self.initial_extensions:
            try:
                if ext not in [extension for extension in self.extensions]:
                    await self.load_extension(ext)
                    print(f"Loaded {ext} cog successfully!")
            except Exception as e:
                print(f"Error loading {ext} cog: {str(e)}")

    async def on_ready(self):
        """
        Event handler for when the bot is ready.
        Prints bot information and syncs commands to guilds.
        """
        print(f"Logged in as {self.user.name}")
        print(f"Bot latency: {round(self.latency * 1000)}ms")
        print(f"Bot is in {len(self.guilds)} guilds.")
        
        # Sync commands to each guild
        print("\nSyncing commands to specific guilds...")
        for guild_id in GUILD_IDS:
            guild = discord.Object(id=guild_id)
            try:
                await self.tree.sync(guild=guild)
                print(f"Successfully synced commands to guild {guild_id}")
            except Exception as e:
                print(f"Error syncing to guild {guild_id}: {str(e)}")

        print("Command synchronization complete!")

    async def on_member_join(self, member: discord.Member):
        """
        Event handler for when a member joins the server.
        Sends a welcome message to the welcome channel.
        """
        print("Someone joined the Discord Server")
        parameter = (f"In under 2000 characters, generate a welcome message for the Largo High School Coding Club. Tell "
                  f"the user {member} a greeting with a {member.mention}. Add this to the message: We accept newbies. "
                  f"Tell them to check out #rules and #roles. Tell them to introduce themselves in #introductions")
        response = gemini_generate(parameter)
        welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
        if welcome_channel:
            await welcome_channel.send(response)

bot = Bot()

@bot.tree.command(name="ping", description="Check the bot's latency")
@app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in GUILD_IDS])
async def ping(interaction: discord.Interaction):
    """Command to check bot's latency/response time"""
    await interaction.response.send_message(f"Pong! Latency: {round(bot.latency * 1000)}ms")

@bot.tree.command(name="hi", description="Say hello to the bot!")
@app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in GUILD_IDS])
async def hi(interaction: discord.Interaction):
    """Friendly greeting command with randomized responses"""
    greetings = ["Hello!", "What's up!", "Howdy!", "Greetings!"]
    response = random.choice(greetings)
    await interaction.response.send_message(response)

@bot.tree.command(name="help", description="Get information about available commands")
@app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in GUILD_IDS])
async def help(interaction: discord.Interaction):
    """Displays help information about available commands"""
    commands = ["/Music", "/Pet", "/Book", "/Video Games", "/PING", "/Job", "/About Me", "/Bye", "/Help", "/Version",
                "/New Stuff", "/Self Destruct", "/Gemini", "/gemini ask", "/gemini explain", "/gemini summarize", "/gemini brainstorm"]
    await interaction.response.send_message(" ".join(commands))

@bot.tree.command(name="bye", description="Say goodbye to the bot!")
@app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in GUILD_IDS])
async def bye(interaction: discord.Interaction):
    """Farewell command with shutdown functionality"""
    await interaction.response.send_message("Goodbye! Shutting down...")
    await bot.close()

@bot.tree.command(name="version", description="Get the current version of the bot")
@app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in GUILD_IDS])
async def version(interaction: discord.Interaction):
    """Displays current bot version information"""
    Version = "3.0"
    DateUpdated = "11/27/2024"
    Language = "Python"
    Discord_API_Wrapper = "Pycord"
    Dev = "D4LM"
    CoDev = "None is the apprentice yet..."
    await interaction.response.send_message("Version: " + Version + "\n" + "Date Updated: " + DateUpdated + "\n" + "Language: " + Language +
                      "\n" + "Developer: " + Dev + "\n" + "Assistant Developer/maintainer: " + CoDev)

@bot.tree.command(name="new_stuff", description="See what's new in the latest update")
@app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in GUILD_IDS])
async def new_stuff(interaction: discord.Interaction):
    """Shows changelog and updates for the latest version"""
    Version = "3.0"
    UpdatedItems = ("Version 3.0 is here!" + "\n" + 
               "* Added Google Calendar integration\n" +
               "* New calendar commands: /events and /add_event\n" +
               "* View and manage your Google Calendar directly from Discord\n" +
               "* Added Gemini AI integration with /gemini ask, /gemini explain, /gemini summarize, and /gemini brainstorm commands\n"
               "* Added Physics and more math commands\n")
    await interaction.response.send_message("For version " + Version + ".\nHere is the Changelog: " + UpdatedItems)

@bot.tree.command(name="self_destruct", description="Shut down the bot dramatically")
@app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in GUILD_IDS])
async def self_destruct(interaction: discord.Interaction):
    """Dramatic shutdown command with countdown"""
    await interaction.response.send_message("💥 SELF DESTRUCT SEQUENCE INITIATED 💥")
    for i in range(5, 0, -1):
        await interaction.channel.send(str(i))
        await asyncio.sleep(1)
    await interaction.channel.send("BOOM! The bot has exploded! 💥")
    await bot.close()

async def on_member_remove(member: discord.Member):
    """
    Event handler for when a member leaves the server.
    Sends a farewell message to the system channel.
    """
    server = member.guild
    question = f"Write a farewell message for {member} leaving."
    response = gemini_generate(question)
    
    if server.system_channel is not None:
       await server.system_channel.send(response)

bot.add_listener(on_member_remove, 'on_member_remove')

def run_bot():
    """Main function to start the bot"""
    bot.run(TOKEN)

if __name__ == "__main__":
    run_bot()
