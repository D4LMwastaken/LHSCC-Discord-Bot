# D4LM's Largo High School Coding Club Discord Bot
A Discord Bot integrated into the Largo High School Coding Club's Discord Server. Actively helps the club run, ultimately allowing people like me (D4LM) avoid overwork by sending some of the workload to this Discord Bot.

## Showcase:
![The user asking what is the meaning of coding.](photos/WhatIsTheMeaningOfCoding.png)

![The slash command toolbar for the bot.](photos/ComandPanelDiscordBot.png)

## Looking for maintainers & co-developers
* If you are interested go to one of the Largo High School Coding Club meetings & talk with one of the leaders.
* We need people like you to help create new ideas, maintain this bot so that D4LM is not overworked making this bot.

## Index
* [Why do I need D4LM's LHSCC Discord Bot?](#why-do-i-need-d4lms-lhscc-discord-bot)
  * [Supported devices](#supported-architecture--devices)
* [Installing D4LM's LHSCC Discord Bot for your own purposes](#installing-d4lms-lhscc-discord-bot)
  * [Windows](#windows-)
  * [Linux](#linux-macos-and-chromeos)
  * [MacOS](#linux-macos-and-chromeos)
  * [ChromeOS](#linux-macos-and-chromeos)
* [Post-installation](#post-installation)
* [Configuration](#configuration)
  * [Creation of new slash commands](#creation-of-new-slash-commands)
* [Troubleshooting](#troubleshooting)
* [Discussion](#discussion)
* [Donate](#donate)
* [Code Contribution](#code-contribution)
* [TODO](#todo)

## Why do I need D4LM's LHSCC Discord Bot?
One of the problems that I have with running a club that is very small is nobody will distribute the workload. For example, my sponsor for my club deos not play a huge role in the club. 

These issues can be mitigated by finding a new sponsor and/or forcing others to do more work. This usually will lead to the collapse of the club very quickly.

Other fixes such as retiring is not an option for me as I am not a senior & the Coding Club will collapse due to lack of leadership.

Given all the above, I needed a simple tool that would reduce my workload & save some time & resources, but allow others to run the club still. That's how D4LM's Largo High School Coding Club Discord Bot was born.

Please note: I would not recommend installing other Discord Bots as this one has many features that could conflict with other Discord Bots.

One bot that does not conflict with D4LM's LHSCC Discord Bot **as of right now** is Crypt's Discord Bot.

### Supported devices
Only devices that support Discord are supported using the bot. You may check this [Discord Article](https://support.discord.com/hc/en-us/articles/213491697-What-are-the-OS-system-requirements-for-Discord).

For running the Discord Bot, here are the minimum specification & recommended specifications:

|                  | Minimum Specification                            | Recommended Specification (From my laptop)                 |
|------------------|--------------------------------------------------|------------------------------------------------------------|
| Operating System | Any that supports Python.                        | Ubuntu 24.04 (Noble Numbat) or any that are still updated. |
| CPU              | x86 & Arm Based.                                 | At least Intel Core i5-5200u or better.                    |
| GPU              | Any as long as it has iGPU.                      | Intel HD Graphics 5500 or better.                          |
| Ram              | 4 MB (Without including OS.                      | 6 GB DDR3L 1600MHz or better.                              |
| Storage          | 200 MB (Without including OS.                    | 384 GB of SSD Sata storage or better.                      |
| Network          | 5 MB/s of download speed 1 MB/s of upload speed. | 300 MB/s of download speed & 10 MB/s of upload Speed.      |

## Features
* Pre-Built Commands
  * `/help` - Display all available commands
  * `/ping` - Check bot's latency
  * `/hi` - Get a friendly greeting
  * `/bye` - Say goodbye to the bot
  * `/version` - Check bot version and info
  * `/new_stuff` - See what's new in the latest version
* Basic Math Operations
  * Addition
  * Subtraction
  * Division
  * Multiplication
* Advanced Gemini AI Integration
* Specific commands for specific use cases
* Calendar Integration
  * Syncs with Google Calendar
  * Event management and scheduling
* Server Management
  * Automatic welcome messages for new members
  * Farewell messages for departing members
* Extensible Architecture
  * Easy to add new commands via cogs
  * Modular design for simple maintenance

## Installing D4LM's LHSCC Discord Bot (outdated)

### Windows 
* Install Python [here](https://www.python.org/).
* Install [Vscode](https://code.visualstudio.com/) or your preferred coding editor or IDE.
#### Install all dependencies
```PowerShell
pip install python-dotenv py-cord google-generativeai
```
* Create a .env file containing this:
``` 
DISCORD_BOT_TOKEN=
GOOGLE_API_KEY=
```
* **Note: You must fill this out: if you don't code will not run**
  * To get the token and the api key go to [Discord's developer portal](https://developers.discord.com) and [Gemini API](https://makersuite.google.com/app/apikey)
  
* Open up your editor's or IDE's terminal inside the project folder, type in
``` PowerShell
python Main.py
```
### Linux, MacOS and ChromeOS
* **Please figure this out yourself, very similar to Window's instruction but there are some differences due to distro, versions, etc.** 
* Note: Might add some if there are people using them and would like to write one...

## Post-installation
* Run `/ping` to verify the bot is responding
  * Initial command load may take a few moments
* Test the Gemini AI integration with `/ask` or `/askpro`
* Verify calendar integration if configured
* Check welcome messages by having a test user join

## Configuration
### Creation of new slash commands
* Navigate to the `cogs` folder
* Create a new Python file for your command(s)
* Follow the existing cog structure (see `Gemini.py` or `Math.py` for examples)
* Import and register your new cog in `Main.py`
* Use proper command decorators and error handling

## Troubleshooting
* Create a new issue, **please add what error you got when you ran it**.

## Discussion
* Go to the Disscussions tab on GitHub to talk with me about it
* If you have LHS Coding Club Discord Server, do that first and message me there

## Donate
* I am a one-man team, please donate, on my wishlist right now is a Framework 16

## Code Contribution
* Fork the GitHub repository, add what you want to add and I might add it if it is very good.
## TODO
* ~~Add stuff to README.MD such as instructions to run & install...~~ About finished...
* ~~Add a way for the Discord bot to greet people who join the Discord Server~~ Finished need to add to GitHub coming soon in 3.0!
* Add a way for the Discord bot to say goodbye to people who leave the Discord Server.
* ~~Allow a way for it to create events...~~ Sync with Google Calendar via API
