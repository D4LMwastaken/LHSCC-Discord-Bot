"""
Google Calendar integration cog for managing calendar events.
This cog provides functionality to view and manage Google Calendar events through Discord commands.
"""

import discord
from discord import app_commands
from discord.ext import commands
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
import datetime

# Define the required Google Calendar API scope
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Calendar(commands.Cog):
    """
    Cog for handling Google Calendar integration.
    Provides commands to view upcoming events and manage calendar entries.
    """
    
    def __init__(self, bot):
        """
        Initialize the Calendar cog.
        
        Args:
            bot (commands.Bot): The bot instance
        """
        self.bot = bot
        self.creds = None
        self.initialize_credentials()

    def initialize_credentials(self):
        """
        Initialize Google Calendar API credentials.
        Handles token refresh and new authentication flow if needed.
        """
        # Check if we have stored credentials
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        # If credentials are invalid or don't exist, refresh or create new ones
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save the credentials for future use
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    @app_commands.command(name="next_event", description="Get the next event from Google Calendar")
    async def next_event(self, interaction: discord.Interaction):
        """
        Get the next upcoming event from the user's Google Calendar.
        
        Args:
            interaction (discord.Interaction): The interaction to respond to
        """
        try:
            await interaction.response.defer()
            
            # Build the Google Calendar service
            service = build('calendar', 'v3', credentials=self.creds)
            
            # Get the current time in UTC
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            
            # Query the calendar API for the next event
            events_result = service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=1,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            # Get the list of events
            events = events_result.get('items', [])
            
            # If no events are found, send a message
            if not events:
                await interaction.followup.send('No upcoming events found.')
                return
                
            # Get the first event
            event = events[0]
            
            # Get the start time of the event
            start = event['start'].get('dateTime', event['start'].get('date'))
            
            # Create the response message
            response = f"Next event: {event['summary']} on {start}"
            
            # Send the response
            await interaction.followup.send(response)
            
        except Exception as e:
            # If an error occurs, send an error message
            await interaction.followup.send(f"An error occurred: {str(e)}")

    @app_commands.command(name="today_events", description="Get today's events from Google Calendar")
    async def today_events(self, interaction: discord.Interaction):
        """
        Get today's events from the user's Google Calendar.
        
        Args:
            interaction (discord.Interaction): The interaction to respond to
        """
        try:
            await interaction.response.defer()
            
            # Build the Google Calendar service
            service = build('calendar', 'v3', credentials=self.creds)
            
            # Get the current date
            today = datetime.datetime.utcnow()
            
            # Get the start and end of the day in UTC
            start_of_day = datetime.datetime(today.year, today.month, today.day, 0, 0, 0).isoformat() + 'Z'
            end_of_day = datetime.datetime(today.year, today.month, today.day, 23, 59, 59).isoformat() + 'Z'
            
            # Query the calendar API for today's events
            events_result = service.events().list(
                calendarId='primary',
                timeMin=start_of_day,
                timeMax=end_of_day,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            # Get the list of events
            events = events_result.get('items', [])
            
            # If no events are found, send a message
            if not events:
                await interaction.followup.send('No events scheduled for today.')
                return
                
            # Create the response message
            response = "Today's events:\n"
            
            # Add each event to the response message
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                response += f"- {event['summary']} at {start}\n"
                
            # Send the response
            await interaction.followup.send(response)
            
        except Exception as e:
            # If an error occurs, send an error message
            await interaction.followup.send(f"An error occurred: {str(e)}")

async def setup(bot):
    """
    Setup the Calendar cog.
    
    Args:
        bot (commands.Bot): The bot instance
    """
    await bot.add_cog(Calendar(bot))