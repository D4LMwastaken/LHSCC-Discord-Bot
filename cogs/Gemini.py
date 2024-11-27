"""
Gemini AI integration cog that provides natural language processing capabilities.
This cog handles all interactions with Google's Gemini-Pro AI model.
"""

import discord
from discord import app_commands
from discord.ext import commands
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables and configure Gemini AI
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# List of guild IDs where the bot will be active
GUILD_IDS = [
    1228003403171627078,
    1239233526835056781
]

def gemini_generate(prompt):
    """
    Generate a response using the Gemini AI model.
    
    Args:
        prompt (str): The input prompt for the AI model
        
    Returns:
        str: The generated response or error message
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def split_response(response, max_length=1800):
    """
    Split a long response into chunks that fit within Discord's message limit.
    
    Args:
        response (str): The full response text to split
        max_length (int): Maximum length for each chunk (default: 1800)
        
    Returns:
        list: List of response chunks
    """
    chunks = []
    current_chunk = ""
    
    # Split by lines to avoid cutting words
    lines = response.split('\n')
    
    for line in lines:
        # If adding this line would exceed the limit, start a new chunk
        if len(current_chunk) + len(line) + 1 > max_length:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = line
        else:
            if current_chunk:
                current_chunk += '\n'
            current_chunk += line
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

class Gemini(commands.GroupCog, group_name="gemini"):
    """
    Cog for handling Gemini AI commands.
    Provides various AI-powered features like asking questions, explaining concepts,
    summarizing text, and brainstorming ideas.
    """
    def __init__(self, bot):
        """
        Initialize the Gemini cog.
        
        Args:
            bot (commands.Bot): The bot instance
        """
        self.bot = bot
        super().__init__()

    async def send_long_response(self, interaction, response):
        """
        Send a response that might be longer than Discord's message limit.
        
        Args:
            interaction (discord.Interaction): The interaction to respond to
            response (str): The response text
        """
        chunks = split_response(response)
        total_chunks = len(chunks)
        
        # Send first chunk
        first_message = chunks[0]
        if total_chunks > 1:
            footer = f"\n\n-# Page 1 of {total_chunks}"
            first_message = first_message + footer
        await interaction.followup.send(first_message)
        
        # Send remaining chunks with message count
        for i, chunk in enumerate(chunks[1:], 2):
            footer = f"\n\n-# Page {i} of {total_chunks}"
            message = chunk + footer
            await interaction.channel.send(message)

    @app_commands.command(name="ask", description="Ask Gemini AI a question")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in GUILD_IDS])
    async def ask(self, interaction: discord.Interaction, question: str):
        """
        Ask Gemini AI a question.
        
        Args:
            interaction (discord.Interaction): The interaction to respond to
            question (str): The question to ask
        """
        try:
            await interaction.response.defer()
            prompt = (f"You are responding to a Discord user. Start your response by mentioning them with {interaction.user.mention}. "
                     f"The question is from {interaction.user.name}: {question}")
            response = gemini_generate(prompt)
            await self.send_long_response(interaction, response)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {str(e)}")

    @app_commands.command(name="explain", description="Ask Gemini AI to explain a concept")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in GUILD_IDS])
    async def explain(self, interaction: discord.Interaction, topic: str):
        """
        Ask Gemini AI to explain a concept.
        
        Args:
            interaction (discord.Interaction): The interaction to respond to
            topic (str): The concept to explain
        """
        try:
            await interaction.response.defer()
            prompt = (f"You are responding to a Discord user. Start your response by mentioning them with {interaction.user.mention}. "
                     f"{interaction.user.name} has asked for an explanation of: {topic}")
            response = gemini_generate(prompt)
            await self.send_long_response(interaction, response)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {str(e)}")

    @app_commands.command(name="summarize", description="Ask Gemini AI to summarize text")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in GUILD_IDS])
    async def summarize(self, interaction: discord.Interaction, text: str):
        """
        Ask Gemini AI to summarize text.
        
        Args:
            interaction (discord.Interaction): The interaction to respond to
            text (str): The text to summarize
        """
        try:
            await interaction.response.defer()
            prompt = (f"You are responding to a Discord user. Start your response by mentioning them with {interaction.user.mention}. "
                     f"{interaction.user.name} has asked for a summary of: {text}")
            response = gemini_generate(prompt)
            await self.send_long_response(interaction, response)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {str(e)}")

    @app_commands.command(name="brainstorm", description="Ask Gemini AI to brainstorm ideas")
    @app_commands.guilds(*[discord.Object(id=guild_id) for guild_id in GUILD_IDS])
    async def brainstorm(self, interaction: discord.Interaction, topic: str):
        """
        Ask Gemini AI to brainstorm ideas.
        
        Args:
            interaction (discord.Interaction): The interaction to respond to
            topic (str): The topic to brainstorm
        """
        try:
            await interaction.response.defer()
            prompt = (f"You are responding to a Discord user. Start your response by mentioning them with {interaction.user.mention}. "
                     f"{interaction.user.name} has asked for a brainstorming session about: {topic}")
            response = gemini_generate(prompt)
            await self.send_long_response(interaction, response)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {str(e)}")

async def setup(bot):
    """
    Set up the Gemini cog.
    
    Args:
        bot (commands.Bot): The bot instance
    """
    await bot.add_cog(Gemini(bot))