"""
Google Calendar integration cog for managing calendar events.
"""

import os
import pytz
import logging
import asyncio

import discord
from discord.ext import commands, tasks
from typing import Optional

from dotenv import load_dotenv
from google.oauth2 import service_account  # Import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get guild IDs from environment variable
GUILD_IDS = [int(guild_id.strip()) for guild_id in os.getenv('GUILD_IDS', '').split(',') if guild_id.strip()]

# Define the required Google Calendar API scope
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',  # Read-only access
    'https://www.googleapis.com/auth/calendar.events'     # Modify events
]

CALENDAR_ID = os.getenv('CALENDAR_ID')

class Calendar(commands.Cog):
    """
    Cog for handling Google Calendar integration.
    """

    def __init__(self, bot):
        """
        Initialize the Calendar cog.
        """
        self.bot = bot
        self.creds = None
        self.service = None  # Store the service object
        self.initialize_credentials()
        self.weekly_announcement.start()

    def cog_unload(self):
        self.weekly_announcement.cancel()

    def initialize_credentials(self):
        """
        Initialize Google Calendar API credentials using a Service Account.
        """
        service_account_file = os.path.join(os.path.dirname(__file__), '..', 'service_account.json')

        self.creds = None

        try:
            if not os.path.exists(service_account_file):
                logger.error(f"Service account file not found at {service_account_file}")
                return  # Exit if file not found

            self.creds = service_account.Credentials.from_service_account_file(
                service_account_file, scopes=SCOPES
            )
            logger.info("Google Calendar credentials loaded from service account file")
            self.service = self.get_google_calendar_service()  # Build service here

        except Exception as e:
            logger.error(f"Error initializing Google Calendar credentials: {e}")
            import traceback
            traceback.print_exc()

    def get_google_calendar_service(self):
        """Build the Google Calendar service."""
        if not self.creds:
            raise ValueError("Could not initialize Google Calendar credentials")
        return build('calendar', 'v3', credentials=self.creds)
    
    async def _get_events(self, days: int):
        """Helper function to fetch events."""
        if not self.service:
            logger.error("Google Calendar service is not initialized.")
            return []

        local_tz = pytz.timezone('US/Eastern')
        now = datetime.now(local_tz)
        end_time = now + timedelta(days=days)

        try:
            events_result = self.service.events().list(
                calendarId=CALENDAR_ID,
                timeMin=now.isoformat(),
                timeMax=end_time.isoformat(),
                maxResults=50,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            return events_result.get('items', [])
        except Exception as e:
            logger.error(f"Error fetching events: {e}")
            return []


    @tasks.loop(hours=24)
    async def weekly_announcement(self):
        """
        Scheduled task that runs every Saturday at 3:00PM EST.
        """
        est = pytz.timezone('US/Eastern')
        current_time = datetime.now(est)
        
        # Check if it's Saturday
        if current_time.weekday() != 5: # != is not equal to...
            return
        
        #Check if it's approimately 3:00PM (Small time window...)
        if not (current_time.hour == 15 and current_time.minute < 15):
            return
        
        logging.info("Running Saturday weekly announcemnt")

    @weekly_announcement.before_loop
    async def before_weekly_announcement(self):
        await self.bot.wait_until_ready()
        
        # Wait until next run time
        est = pytz.timezone('US/Eastern')
        now = datetime.now(est)
        
        # Calculate days until next Saturday
        days_until_saturday = (5 - now.weekday()) % 7
        
        # If it's Saturday but after 3 PM, wait until next Saturday
        if days_until_saturday == 0 and now.hour >= 15:
            days_until_saturday = 7
                
        target_time = now.replace(
            day=now.day + days_until_saturday,
            hour=15, 
            minute=0, 
            second=0, 
            microsecond=0
            )
            
        seconds_to_wait = (target_time - now).total_seconds()
        if seconds_to_wait > 0:
            logging.info(f"Waiting {seconds_to_wait/3600:.1f} hours until next Saturday 3 PM")
            await asyncio.sleep(seconds_to_wait)

    @commands.slash_command(name="upcoming", guild_ids=GUILD_IDS)
    async def upcoming_events(self, ctx, days: Optional[int] = 7):
        """Retrieve upcoming events from Google Calendar."""
        await ctx.defer()

        events = await self._get_events(days)
        if not events:
            await ctx.respond(f"No upcoming events in the next {days} days.")
            return

        embed = discord.Embed(
            title=f"Upcoming Events (Next {days} Days)",
            color=discord.Color.blue()
        )

        local_tz = pytz.timezone('US/Eastern')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_time = datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone(local_tz)
            formatted_date = start_time.strftime("%A, %B %d at %I:%M %p %Z")
            embed.add_field(
                name=event.get('summary', 'Untitled Event'),
                value=formatted_date,
                inline=False
            )

        await ctx.respond(embed=embed)

    @commands.slash_command(name="add", guild_ids=GUILD_IDS)
    async def add_event(self, ctx, title: str, date: str, time: Optional[str] = None):
        """Add a new event to Google Calendar."""
        await ctx.defer()

        if not self.service:
            await ctx.respond("Google Calendar service is not initialized.")
            return

        local_tz = pytz.timezone('US/Eastern')

        try:
            if time:
                event_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            else:
                event_datetime = datetime.strptime(date, "%Y-%m-%d")
                event_datetime = event_datetime.replace(hour=12, minute=0)  # Default to noon

            event_datetime = local_tz.localize(event_datetime)

            event = {
                'summary': title,
                'start': {
                    'dateTime': event_datetime.isoformat(),
                    'timeZone': str(local_tz),
                },
                'end': {
                    'dateTime': (event_datetime + timedelta(hours=1)).isoformat(),
                    'timeZone': str(local_tz),
                },
            }

            event = self.service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
            await ctx.respond(f"Event '{title}' added successfully on {event_datetime.strftime('%Y-%m-%d')}")

        except ValueError:
            await ctx.respond("Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time.")
        except Exception as e:
            logger.error(f"Error adding event: {e}")
            await ctx.respond(f"An error occurred: {str(e)}")
    @commands.slash_command(name="announce_events", guild_ids=GUILD_IDS)
    async def announce_events(self, ctx):
        """
        Manually trigger the weekly event announcement.
        """
        if not ctx.channel.permissions_for(ctx.author).administrator:
            await ctx.respond("You need administrator permissions to use this command.", ephemeral=True)
            return

        await ctx.defer()
        events = await self._get_events(7)
        
        if not events:
            await ctx.respond("No upcoming events found for the next 7 days.")
            return
            
        est = pytz.timezone('US/Eastern')
        now = datetime.now(est)
        # Create the announcement embed
        embed = discord.Embed(
            title="📅 Upcoming Events This Week",
            description="Here are the events scheduled for the next 7 days:",
            color=discord.Color.blue(),
            timestamp=now
        )
        
        # Add events to the embed
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_time = datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone(est)
            
            # Format the date and time
            formatted_date = start_time.strftime("%A, %B %d at %I:%M %p %Z")
            
            embed.add_field(
                name=event.get('summary', 'Untitled Event'),
                value=f"📆 {formatted_date}\n{event.get('description', 'No description available')}",
                inline=False
            )
        
        embed.set_footer(text="Manually triggered announcement")
        
        # Find the announcements channel and send the message
        announcements_channel = discord.utils.get(ctx.guild.text_channels, name="announcements")
        if announcements_channel:
            await announcements_channel.send("<@&1236351432865611968>", embed=embed) # Changed to only send it to the active group...
            await ctx.respond("Weekly announcement sent successfully!", ephemeral=True)
        else:
            await ctx.respond("Could not find #announcements channel.", ephemeral=True)

def setup(bot):
    """
    Set up the Calendar Cog.
    """
    pass  # Cog is now added in Main.py __init__ method
