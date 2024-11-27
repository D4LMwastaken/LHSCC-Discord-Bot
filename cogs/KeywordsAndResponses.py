"""
Keywords and Responses Cog for Discord Bot
This module handles casual conversation responses for various topics.
Provides engaging and friendly responses to common conversation topics.
"""

import discord
from discord import app_commands
from discord.ext import commands
import random

# Predefined responses for different conversation topics
music_responses = [
    "I love listening to all kinds of music! What's your favorite genre?",
    "Music is the universal language that connects us all!",
    "Nothing beats a good melody to lift your spirits!",
    "From classical to rock, every genre has its own unique beauty."
]

pet_responses = [
    "Pets are wonderful companions! Do you have any?",
    "Dogs, cats, or maybe something more exotic?",
    "Animals bring so much joy to our lives!",
    "I'd love to hear about your pets!"
]

book_responses = [
    "Reading opens up whole new worlds!",
    "Books are a great way to learn and explore!",
    "What's your favorite book genre?",
    "Nothing beats curling up with a good book!"
]

video_game_responses = [
    "Gaming is such a fun way to spend time!",
    "What games have you been playing lately?",
    "From indie to AAA, there's something for everyone!",
    "Games are a great way to challenge yourself and have fun!"
]

job_responses = [
    "Every job has its own unique challenges and rewards!",
    "What field are you interested in?",
    "The tech industry is always evolving!",
    "It's important to find work that you're passionate about!"
]

about_me_responses = [
    "I'm a friendly Discord bot here to help!",
    "I love learning new things and chatting with users!",
    "My purpose is to make this server more fun and interactive!",
    "I'm always being updated with new features!"
]

def get_random_response(responses):
    """
    Get a random response from a list of predefined responses.
    
    Args:
        responses (list): List of possible responses
        
    Returns:
        str: Randomly selected response
    """
    return random.choice(responses)

class KeywordsAndResponses(commands.Cog):
    """
    Cog for handling casual conversation commands.
    Provides friendly responses to various topics like music, pets, books, etc.
    """
    def __init__(self, bot):
        """
        Initialize the KeywordsAndResponses Cog.
        
        Args:
            bot (commands.Bot): The bot instance
        """
        self.bot = bot

    @app_commands.command(name="music", description="Talk about music")
    async def music(self, interaction: discord.Interaction):
        """
        Send a random music-related response.
        
        Args:
            interaction (discord.Interaction): The interaction instance
        """
        await interaction.response.send_message(get_random_response(music_responses))

    @app_commands.command(name="pet", description="Talk about pets")
    async def pet(self, interaction: discord.Interaction):
        """
        Send a random pet-related response.
        
        Args:
            interaction (discord.Interaction): The interaction instance
        """
        await interaction.response.send_message(get_random_response(pet_responses))

    @app_commands.command(name="book", description="Talk about books")
    async def book(self, interaction: discord.Interaction):
        """
        Send a random book-related response.
        
        Args:
            interaction (discord.Interaction): The interaction instance
        """
        await interaction.response.send_message(get_random_response(book_responses))

    @app_commands.command(name="video_games", description="Talk about video games")
    async def video_games(self, interaction: discord.Interaction):
        """
        Send a random video game-related response.
        
        Args:
            interaction (discord.Interaction): The interaction instance
        """
        await interaction.response.send_message(get_random_response(video_game_responses))

    @app_commands.command(name="job", description="Talk about jobs")
    async def job(self, interaction: discord.Interaction):
        """
        Send a random job-related response.
        
        Args:
            interaction (discord.Interaction): The interaction instance
        """
        await interaction.response.send_message(get_random_response(job_responses))

    @app_commands.command(name="about_me", description="Learn about the bot")
    async def about_me(self, interaction: discord.Interaction):
        """
        Send a random response about the bot.
        
        Args:
            interaction (discord.Interaction): The interaction instance
        """
        await interaction.response.send_message(get_random_response(about_me_responses))

async def setup(bot):
    """
    Set up the KeywordsAndResponses Cog.
    
    Args:
        bot (commands.Bot): The bot instance
    """
    await bot.add_cog(KeywordsAndResponses(bot))
