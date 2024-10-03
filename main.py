import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# load .env
load_dotenv()

# secret token to access bot (Never share this)
TOKEN = os.getenv('DISCORD_TOKEN')

# select intents the bot needs in order to work
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Print to console when bot is ready and send Online message to channel
# TODO: filter channel ID dynamically/provide way to change channelID
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    channel = bot.get_channel(1291174504382595206)

    if channel:
        await channel.send("Hi! The OOP-Helper Bot is online now!")

# Test command
@bot.command(name="greet")
async def greet(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")


bot.run(TOKEN)

