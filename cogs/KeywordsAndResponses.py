"""
Keywords and Responses Cog for Discord Bot
This module manages keywords and their associated responses using a JSON file.
"""

import discord
from discord.ext import commands
import json
import os
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get guild IDs from environment variable
GUILD_IDS = [int(guild_id.strip()) for guild_id in os.getenv('GUILD_IDS', '').split(',') if guild_id.strip()]

# Path to the keywords JSON file
KEYWORDS_FILE = os.path.join(os.path.dirname(__file__), 'keywords.json')

def load_keywords():
    """
    Load keywords and responses from the JSON file.
    
    Returns:
        dict: Dictionary of keywords and their responses
    """
    try:
        with open(KEYWORDS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_keywords(keywords):
    """
    Save keywords and responses to the JSON file.
    
    Args:
        keywords (dict): Dictionary of keywords and their responses
    """
    with open(KEYWORDS_FILE, 'w') as f:
        json.dump(keywords, f, indent=4)

class KeywordsAndResponses(commands.Cog):
    """
    Cog for managing keywords and custom responses.
    Allows adding, removing, updating, and listing keywords.
    """
    
    def __init__(self, bot):
        """
        Initialize the Keywords and Responses cog.
        
        Args:
            bot (commands.Bot): The bot instance
        """
        self.bot = bot
        self.keywords = load_keywords()
        
        # Create the command group within the class
        self.keyword_group = bot.create_group(name="keyword", description="Manage keywords and responses")

        # Dynamically add commands to the group
        self.keyword_group.command(name="add")(self.add_keyword)
        self.keyword_group.command(name="remove")(self.remove_keyword)
        self.keyword_group.command(name="update")(self.update_keyword)
        self.keyword_group.command(name="list")(self.list_keywords)

    async def add_keyword(self, ctx, keyword: str, response: str):
        """
        Add a new keyword and its response.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            keyword (str): The keyword to add
            response (str): The response associated with the keyword
        """
        try:
            # Check if keyword already exists
            if keyword.lower() in self.keywords:
                await ctx.respond(f"Keyword '{keyword}' already exists. Use /keyword update to modify it.")
                return
            
            # Add keyword to dictionary
            self.keywords[keyword.lower()] = response
            save_keywords(self.keywords)
            
            await ctx.respond(f"Keyword '{keyword}' added successfully!")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def remove_keyword(self, ctx, keyword: str):
        """
        Remove a keyword.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            keyword (str): The keyword to remove
        """
        try:
            # Check if keyword exists
            if keyword.lower() not in self.keywords:
                await ctx.respond(f"Keyword '{keyword}' not found.")
                return
            
            # Remove keyword from dictionary
            del self.keywords[keyword.lower()]
            save_keywords(self.keywords)
            
            await ctx.respond(f"Keyword '{keyword}' removed successfully!")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def update_keyword(self, ctx, keyword: str, new_response: str):
        """
        Update an existing keyword's response.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            keyword (str): The keyword to update
            new_response (str): The new response for the keyword
        """
        try:
            # Check if keyword exists
            if keyword.lower() not in self.keywords:
                await ctx.respond(f"Keyword '{keyword}' not found. Use /keyword add to create it.")
                return
            
            # Update keyword response
            self.keywords[keyword.lower()] = new_response
            save_keywords(self.keywords)
            
            await ctx.respond(f"Keyword '{keyword}' updated successfully!")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def list_keywords(self, ctx):
        """
        List all current keywords.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
        """
        try:
            # Check if keywords dictionary is empty
            if not self.keywords:
                await ctx.respond("No keywords have been added yet.")
                return
            
            # Create a formatted list of keywords
            keyword_list = "\n".join([f"• {k}: {v}" for k, v in self.keywords.items()])
            
            # Send the list of keywords
            await ctx.respond(f"Current Keywords:\n{keyword_list}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Listener to check for keywords in messages.
        
        Args:
            message (discord.Message): The message to check
        """
        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return
        
        # Convert message content to lowercase
        content = message.content.lower()
        
        # Check for keywords
        for keyword, response in self.keywords.items():
            if keyword in content:
                # Randomly choose a response if multiple are available
                if isinstance(response, list):
                    response = random.choice(response)
                
                await message.channel.send(response)
                break

def setup(bot):
    """
    Set up the Keywords and Responses Cog.
    
    Args:
        bot (commands.Bot): The bot instance
    """
    pass  # Cog is now added in Main.py __init__ method
