import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    channel = bot.get_channel(1291174504382595206)

    if channel:
        await channel.send("Hi! The OOP-Helper Bot is online now!")


@bot.command(name="greet")
async def greet(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")


bot.run(TOKEN)

