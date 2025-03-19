"""
Gemini AI integration cog that provides natural language processing capabilities.
This cog handles all interactions with Google's Gemini-Pro AI model.
"""

from discord.ext import commands
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get guild IDs from environment variable
GUILD_IDS = [int(guild_id.strip()) for guild_id in os.getenv('GUILD_IDS', '').split(',') if guild_id.strip()]

# Get Google API key from environment variable
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-pro-exp-02-05')

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
    # Split the response into chunks
    chunks = []
    current_chunk = ""
    
    # Split response into words to avoid breaking words
    words = response.split()
    
    for word in words:
        # If adding this word would exceed max length, start a new chunk
        if len(current_chunk) + len(word) + 1 > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = ""
        
        # Add word to current chunk
        current_chunk += word + " "
    
    # Add the last chunk if not empty
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

class Gemini(commands.Cog):
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

    @commands.slash_command(name="ask", guild_ids=GUILD_IDS)
    async def ask(self, ctx, question: str):
        """
        Ask Gemini AI a question.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            question (str): The question to ask
        """
        await ctx.defer()  # Defer the response to handle longer processing times
        try:
            # Generate response using Gemini AI
            response = gemini_generate(question)
            
            # Split response if it's too long
            response_chunks = split_response(response)
            
            # Send the first chunk
            if response_chunks:
                await ctx.respond(response_chunks[0])
                
                # Send additional chunks if they exist
                for chunk in response_chunks[1:]:
                    await ctx.send(chunk)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    @commands.slash_command(name="explain", guild_ids=GUILD_IDS)
    async def explain(self, ctx, topic: str):
        """
        Ask Gemini AI to explain a concept.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            topic (str): The topic to explain
        """
        await ctx.defer()  # Defer the response to handle longer processing times
        try:
            # Generate explanation using Gemini AI
            prompt = f"Explain the concept of {topic} in a clear and concise manner."
            response = gemini_generate(prompt)
            
            # Split response if it's too long
            response_chunks = split_response(response)
            
            # Send the first chunk
            if response_chunks:
                await ctx.respond(response_chunks[0])
                
                # Send additional chunks if they exist
                for chunk in response_chunks[1:]:
                    await ctx.send(chunk)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    @commands.slash_command(name="summarize", guild_ids=GUILD_IDS)
    async def summarize(self, ctx, text: str):
        """
        Ask Gemini AI to summarize a given text.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            text (str): The text to summarize
        """
        await ctx.defer()  # Defer the response to handle longer processing times
        try:
            # Generate summary using Gemini AI
            prompt = f"Summarize the following text concisely: {text}"
            response = gemini_generate(prompt)
            
            # Split response if it's too long
            response_chunks = split_response(response)
            
            # Send the first chunk
            if response_chunks:
                await ctx.respond(response_chunks[0])
                
                # Send additional chunks if they exist
                for chunk in response_chunks[1:]:
                    await ctx.send(chunk)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    @commands.slash_command(name="brainstorm", guild_ids=GUILD_IDS)
    async def brainstorm(self, ctx, topic: str):
        """
        Ask Gemini AI to brainstorm ideas.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            topic (str): The topic to brainstorm
        """
        await ctx.defer()  # Defer the response to handle longer processing times
        try:
            # Generate brainstorming ideas using Gemini AI
            prompt = f"Provide a list of creative ideas or potential approaches for the following topic: {topic}"
            response = gemini_generate(prompt)
            
            # Split response if it's too long
            response_chunks = split_response(response)
            
            # Send the first chunk
            if response_chunks:
                await ctx.respond(response_chunks[0])
                
                # Send additional chunks if they exist
                for chunk in response_chunks[1:]:
                    await ctx.send(chunk)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    @commands.slash_command(name="code_help", guild_ids=GUILD_IDS)
    async def code_help(self, ctx, language: str, problem: str):
        """
        Ask Gemini AI for coding help.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            language (str): The programming language
            problem (str): Description of the coding problem
        """
        await ctx.defer()  # Defer the response to handle longer processing times
        try:
            # Generate code help using Gemini AI
            prompt = f"Provide a solution in {language} for the following coding problem: {problem}"
            response = gemini_generate(prompt)
            
            # Split response if it's too long
            response_chunks = split_response(response)
            
            # Send the first chunk
            if response_chunks:
                await ctx.respond(response_chunks[0])
                
                # Send additional chunks if they exist
                for chunk in response_chunks[1:]:
                    await ctx.send(chunk)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

def setup(bot):
    """
    Set up the Gemini Cog.
    
    Args:
        bot (commands.Bot): The bot instance
    """
    pass  # Cog is now added in Main.py __init__ method
