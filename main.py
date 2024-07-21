import discord
from discord.ext import commands
import os
import logging
import json
import utils
from dotenv import load_dotenv
load_dotenv(override=True)
#Bot configuration
prefix = "!"

application_id = os.getenv("APPLICATION_ID")
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=prefix, intents=intents, application_id=application_id)    
bot.settings = utils.load_settings()

# Load cogs from the commands and events directories
async def load_extensions():
    for folder in ['commands', 'events']:
        for filename in os.listdir(f'./cogs/{folder}'):
            if filename.endswith('.py') and filename != '__init__.py':
                try:
                    await bot.load_extension(f'cogs.{folder}.{filename[:-3]}')
                    #print(f'Loaded extension: {filename}')
                    logger.info(f'Loaded extension: {filename}')
                except Exception as e:
                    #print(f'Failed to load extension {filename}: {e}')
                    logger.error(f'Failed to load extension {filename}: {e}')

@bot.event
async def on_ready():
    #print(f'Logged on as {self.user}')
    logger.info(f'Logged on as {bot.user}')
    await load_extensions()

@bot.before_invoke
async def before_invoke(ctx):
    ctx.settings = bot.settings



bot.run(os.getenv("BOTTOKEN"))
