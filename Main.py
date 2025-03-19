"""
Main bot file that handles initialization, commands, and event listeners.
This file serves as the entry point for the Discord bot and manages core functionality.
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import random
import logging

""" Comment notes:
* noqa means inspection is disabled on that line
"""

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s' # noqa
)

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
APPLICATION_ID = os.getenv('DISCORD_APPLICATION_ID')

# List of guild IDs where the bot will be active
GUILD_IDS = [int(guild_id.strip()) for guild_id in os.getenv('GUILD_IDS', '').split(',') if guild_id.strip()]

class Bot(commands.Bot):
    """
    Main bot class that inherits from commands.Bot.
    Handles initialization of cogs and core bot functionality.
    """
    def __init__(self):
        """
        Create bot instance with intents and load initial extensions.
        """
        # Create bot instance with intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True  # Enable member events
        super().__init__(command_prefix='!', intents=intents, application_id=APPLICATION_ID)
        
        # Dynamically find all cogs in the cogs directory
        self.initial_extensions = []
        cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')
        for filename in os.listdir(cogs_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = f'cogs.{filename[:-3]}'
                self.initial_extensions.append(module_name)
        
        # Dynamically import and add cogs
        for module_name in self.initial_extensions:
            try:
                module = __import__(module_name, fromlist=['setup'])
                
                # Check if the module has a setup function
                if hasattr(module, 'setup'):
                    # Find the cog class dynamically
                    cog_classes = [getattr(module, name) for name in dir(module) 
                                   if isinstance(getattr(module, name), type) and 
                                   issubclass(getattr(module, name), commands.Cog) and 
                                   getattr(module, name) is not commands.Cog]
                    
                    if cog_classes:
                        cog_class = cog_classes[0]
                        self.add_cog(cog_class(self))
                        print(f"Loaded {module_name} cog successfully!")
                    else:
                        print(f"No Cog class found in {module_name}")
                else:
                    print(f"No setup function found in {module_name}")
            except Exception as e:
                print(f"Error loading {module_name} cog: {str(e)}")
                import traceback
                traceback.print_exc()

    async def setup_hook(self):
        """
        Loads all cogs during bot startup using Pycord's extension loading.
        Prints success/error messages for each cog loading attempt.
        """
        try:
            # Sync commands globally to ensure all slash commands are registered
            print("Syncing global slash commands...")
            
            # Get all registered commands before sync
            before_commands = await self.fetch_commands() # noqa
            print(f"Commands before sync: {[cmd.name for cmd in before_commands]}")
            
            # Sync commands with more verbose logging
            synced_commands = await self.sync_commands(force=True)
            print(f"Synced commands: {[cmd.name for cmd in synced_commands]}") # noqa
            
            # Get all registered commands after sync
            after_commands = await self.fetch_commands() # noqa
            print(f"Commands after sync: {[cmd.name for cmd in after_commands]}")
        
        except Exception as e:
            print(f"Error in setup_hook: {e}")
            import traceback
            traceback.print_exc()

    async def on_ready(self):
        """
        Event handler for when the bot is ready and connected to Discord.
        Loads initial extensions and sets up bot status.
        """
        try:
            # Set bot's status
            await self.change_presence(
                status=discord.Status.online, 
                activity=discord.Game(name="Helping Largo High School Coding Club")
            )
            
            print(f'Logged in as {self.user} (ID: {self.user.id})') #noqa
            print('------')
        
        except Exception as e:
            print(f"An error occurred during bot setup: {e}")
            import traceback
            traceback.print_exc()

    async def on_member_join(self, member: discord.Member):
        """
        Event handler for when a new member joins the server.
        Sends a welcome message to the system channel using Gemini API.
        
        Args:
            member (discord.Member): The member who joined the server
        """
        try:
            # Try to get the system channel of the guild
            system_channel = member.guild.system_channel
            
            if system_channel:
                # Generate welcome message using Gemini
                from cogs.Gemini import gemini_generate
                
                # Craft a prompt to generate a personalized welcome message
                welcome_prompt = (
                    f"Generate a warm, engaging welcome message for a new member named {member.name} "
                    f"joining the Largo High School Coding Club Discord server. "
                    "The message should be friendly, encouraging, and include:"
                    "- A personalized greeting"
                    "- Encouragement to explore the server"
                    "- Suggestion to check out #announcements and #roles"
                    "- Invitation to introduce themselves"
                    "Keep the tone friendly, supportive, and exciting for a high school coding club. "
                    "Limit the message to 250 words."
                )
                
                # Generate welcome message
                welcome_text = gemini_generate(welcome_prompt)
                
                # Create a welcoming embed
                welcome_embed = discord.Embed(
                    title="Welcome to the Largo High School Coding Club!",
                    description=welcome_text,
                    color=discord.Color.green()
                )
                
                # Set the member's avatar as the thumbnail
                welcome_embed.set_thumbnail(url=member.display_avatar.url)
                
                # Add a footer with additional guidance
                welcome_embed.set_footer(text="Tip: Check out our channels and introduce yourself!")
                
                # Send the welcome message
                await system_channel.send(f"{member.mention}", embed=welcome_embed)
                
                logging.info(f"Sent Gemini-generated welcome message for {member.name} in {member.guild.name}")
            else:
                logging.warning(f"No system channel found in {member.guild.name}")
        
        except Exception as e:
            logging.error(f"Error sending welcome message: {e}")
            import traceback
            traceback.print_exc()

    async def on_member_remove(self, member: discord.Member):
        """
        Event handler for when a member leaves the server.
        Sends a farewell message to the system channel using Gemini API.
        
        Args:
            member (discord.Member): The member who left the server
        """
        try:
            # Try to get the system channel of the guild
            system_channel = member.guild.system_channel
            
            if system_channel:
                # Generate farewell message using Gemini
                from cogs.Gemini import gemini_generate
                
                # Craft a prompt to generate a personalized farewell message
                farewell_prompt = (
                    f"Generate a thoughtful, kind farewell message for a member named {member.name} "
                    f"who is leaving the Largo High School Coding Club Discord server. "
                    "The message should be:"
                    "- Respectful and understanding"
                    "- Acknowledging their time in the community"
                    "- Wishing them well in future endeavors"
                    "- Leaving the door open for potential return"
                    "Keep the tone warm, supportive, and positive. "
                    "Limit the message to 250 words."
                )
                
                # Generate farewell message
                farewell_text = gemini_generate(farewell_prompt)
                
                # Create a farewell embed
                farewell_embed = discord.Embed(
                    title="Farewell from Largo High School Coding Club",
                    description=farewell_text,
                    color=discord.Color.red()
                )
                
                # Set a default avatar if member has left
                farewell_embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
                
                # Add a footer with a supportive message
                farewell_embed.set_footer(text="We hope to see you again in the future!")
                
                # Send the farewell message
                await system_channel.send(embed=farewell_embed)
                
                logging.info(f"Sent Gemini-generated farewell message for {member.name} in {member.guild.name}")
            else:
                logging.warning(f"No system channel found in {member.guild.name}")
        
        except Exception as e:
            logging.error(f"Error sending farewell message: {e}")
            import traceback
            traceback.print_exc()

bot = Bot()

@bot.slash_command(name="ping", description="Check the bot's latency", guild_ids=GUILD_IDS)
async def ping(interaction: discord.Interaction):
    """Command to check bot's latency/response time"""
    await interaction.response.send_message(f"Pong! Latency: {round(bot.latency * 1000)}ms")

@bot.slash_command(name="hi", description="Say hello to the bot!", guild_ids=GUILD_IDS)
async def hi(interaction: discord.Interaction):
    """Friendly greeting command with randomized responses"""
    greetings = ["Hello!", "What's up!", "Howdy!", "Greetings!"]
    response = random.choice(greetings)
    await interaction.response.send_message(response)

@bot.slash_command(name="help", description="Get information about available commands", guild_ids=GUILD_IDS)
async def help(interaction: discord.Interaction):
    """Displays help information about available commands"""
    commands = ["/Music", "/Pet", "/Book", "/Video Games", "/PING", "/Job", "/About Me", "/Bye", "/Help", "/Version",
                "/New Stuff", "/Self Destruct", "/Gemini", "/gemini ask", "/gemini explain", "/gemini summarize", "/gemini brainstorm"]
    await interaction.response.send_message(" ".join(commands))

@bot.slash_command(name="bye", description="Say goodbye to the bot!", guild_ids=GUILD_IDS)
async def bye(interaction: discord.Interaction):
    """Farewell command with shutdown functionality"""
    await interaction.response.send_message("Goodbye! Shutting down...")
    await bot.close()

@bot.slash_command(name="version", description="Get the current version of the bot", guild_ids=GUILD_IDS)
async def version(interaction: discord.Interaction):
    """Displays current bot version information"""
    Version = "3.2"
    DateUpdated = "3/19/2025"
    Language = "Python"
    Discord_API_Wrapper = "Pycord"
    Dev = "D4LM"
    CoDev = "None is the apprentice yet..."
    await interaction.response.send_message("Version: " + Version + "\n" + "Date Updated: " + DateUpdated + "\n" + "Language: " + Language +
                      "\n" + "Disocrd API Wrapper: " + Discord_API_Wrapper + "\n" + "Developer: " + Dev + "\n" + "Assistant Developer/Mentor: "
                      + CoDev)

@bot.slash_command(name="new_stuff", description="See what's new in the latest update", guild_ids=GUILD_IDS)
async def new_stuff(interaction: discord.Interaction):
    """Shows changelog and updates for the latest version"""
    Version = "3.0"
    UpdatedItems = ("Changes in version 3.2:\n"
                "* Security fixes\n"
                "* Calendar API now uses service account so that calendar commands can run forever(hopefully)...\n"
                "* General cleanup...\n")
    await interaction.response.send_message("For version " + Version + ".\nHere is the Changelog: " + UpdatedItems)

@bot.slash_command(name="self_destruct", description="Shut down the bot dramatically", guild_ids=GUILD_IDS)
async def self_destruct(interaction: discord.Interaction):
    """Dramatic shutdown command with countdown"""
    await interaction.response.send_message("💥 SELF DESTRUCT SEQUENCE INITIATED 💥")
    for i in range(5, 0, -1):
        await interaction.channel.send(str(i)) #noqa
        await asyncio.sleep(1)
    await interaction.channel.send("BOOM! The bot has exploded! 💥") #noqa
    await bot.close()

@bot.slash_command(name="rate_limit_status", description="Check Discord API rate limit status", guild_ids=GUILD_IDS)
async def rate_limit_status(interaction: discord.Interaction):
    """
    Check the bot's current rate limit status and latency.
    
    Args:
        interaction (discord.Interaction): The interaction to respond to
    """
    try:
        # Calculate bot latency
        latency = round(bot.latency * 1000, 2)  # Convert to milliseconds
        
        # Assess rate limit risk based on latency
        if latency < 50:
            risk_level = "Low"
            color = discord.Color.green()
        elif 50 <= latency < 150:
            risk_level = "Moderate"
            color = discord.Color.yellow()
        else:
            risk_level = "High"
            color = discord.Color.red()
        
        # Create an embed to display rate limit status
        embed = discord.Embed(
            title="🚦 Bot Rate Limit Status",
            description="Current performance metrics for the Discord bot",
            color=color
        )
        embed.add_field(name="Latency", value=f"{latency} ms", inline=False)
        embed.add_field(name="Risk Level", value=risk_level, inline=False)
        
        # Add recommendations based on risk level
        if risk_level == "Low":
            embed.add_field(name="Status", value="✅ Bot is performing optimally", inline=False)
        elif risk_level == "Moderate":
            embed.add_field(name="Recommendation", value="⚠️ Monitor bot performance", inline=False)
        else:
            embed.add_field(name="Recommendation", value="🛑 Consider reducing bot load or checking network", inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    except Exception as e:
        await interaction.response.send_message(f"An error occurred while checking rate limit status: {str(e)}")

def run_bot():
    """Main function to start the bot"""
    bot.run(TOKEN)

if __name__ == "__main__":
    run_bot()
