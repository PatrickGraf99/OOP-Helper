import os

import discord
from logger import Logger
from discord.ext import commands
from dotenv import load_dotenv

from datetime import datetime
import pytz

# TODO Refactor so Bot is a class???

# load .env
load_dotenv()


# secret token to access bot (Never share this)
TOKEN: str = os.getenv('DISCORD_TOKEN')

# select intents the bot needs in order to work (not sure about which ones are really needed)
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
intents.guilds = True

# If channel ID is from a Server without the bot, bot.get_channel apparently returns None
dm_channel_id: int = -99

bot = commands.Bot(command_prefix='!', intents=intents)


# Print to console when bot is ready and send Online message to channel
# TODO: filter channel ID dynamically/provide way to change channelID
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


# Credits: https://stackoverflow.com/questions/65062678/how-to-make-my-bot-forward-dms-sent-to-it-to-a-channel
@bot.event
async def on_message(message):
    # Logic for when message is received in dm and the message was not authored by the bot itself
    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        # TODO: implement logger
        # Get current datetime and format it
        now: datetime = datetime.now(pytz.timezone('Europe/Berlin'))
        formatted_time: str = now.strftime("%d.%m.%Y %H:%M")
        timestamp: float = now.timestamp()
        print(f'{message.author.name} sent message {message.content} at {formatted_time}')
        # Reply to user if there is no dm_channel set
        if dm_channel_id == -99:
            await message.channel.send('Sorry, there is currently no redirect channel. Please try again later')
        else:
            target_channel = bot.get_channel(dm_channel_id)
            print(f'Forwarding message to channel ID {target_channel.id}')
            # Send content of DM back to specified dm-channel
            await target_channel.send(message.content)
    # Processing message so commands will work
    await bot.process_commands(message)


# Set Channel for Questions
@bot.command(name='dm-channel', help='Sets the channel where bot DMs will be redirected to')
@commands.has_permissions(administrator=True)
async def set_dm_channel(ctx, channel_name=''):
    # Send syntax hint if no channel name was specified
    if channel_name == '':
        await ctx.send('Command Syntax: !dm-channel <channel_name>')
        return
    guild: discord.Guild = ctx.guild
    channel: discord.TextChannel = discord.utils.get(guild.text_channels, name=channel_name)
    # Send error hint if channel does not exist
    if channel is None:
        await ctx.send(f'Found no channel \"{channel_name}\"')
        return
    # Use global so dm_channel_id is properly updated and set new ID
    global dm_channel_id
    dm_channel_id = channel.id
    await ctx.send(f'Set channel where DMs will be redirected to to {dm_channel_id}')

bot.run(TOKEN)
