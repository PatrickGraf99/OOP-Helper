import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from logger import Logger


class OOPBot:
    def __init__(self, logging=False):
        # dotenv loading
        load_dotenv()
        self.DISCORD_TOKEN: str = os.getenv('DISCORD_TOKEN')

        # bot and log setup
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.logger: Logger = Logger('log.json')
        self.logging_active: bool = logging

        # TODO: Make a config file where stuff like this can be stored
        self.dm_channel_id: int = -99

        self.__register_events__()
        self.__register_commands__()

    def __register_events__(self) -> None:

        @self.bot.event
        async def on_ready() -> None:
            print(f'Logged in as {self.bot.user}')

        @self.bot.event
        async def on_message(message: discord.Message) -> None:
            # Ignore if bot itself sent the message
            if message.author == self.bot.user:
                await self.bot.process_commands(message)
                return

            # Ignore all messages that are not being sent via DMs
            if not isinstance(message.channel, discord.DMChannel):
                await self.bot.process_commands(message)
                return
            if self.dm_channel_id == -99:
                print('Bot can\'t redirect DMs since there is no channel set')
                # await message.channel.send('Sorry, there is currently no redirect channel. Please try again later')
            else:
                target_channel = self.bot.get_channel(self.dm_channel_id)
                await target_channel.send(f'Forwarded Message:\n {message.content}')
            if self.logging_active:
                self.logger.log_dm(message)
            await self.bot.process_commands(message)

    def __register_commands__(self) -> None:

        @self.bot.command(name='dm-channel', help='Sets the channel where bot Dms will be redirected to\n'
                                                  'Usage: !dm-channel <channel>')
        @commands.has_permissions(administrator=True)
        async def dm_channel(ctx: commands.Context, channel_name='') -> None:
            if channel_name == '':
                await ctx.send('Please enter a channel name; !dm-channel <channel_name>')
                return
            guild: discord.Guild = ctx.guild
            # TODO Use category in combination with channel name to uniquely identify the channel
            channel: discord.TextChannel = discord.utils.get(guild.text_channels, name=channel_name)
            if channel is None:
                await ctx.send(f'Sorry, I couldn\'t find the channel \"{channel_name}\"')
                return
            self.dm_channel_id = channel.id
            await ctx.send(f'All DMs the bot receives will be redirected to {channel.mention} (ID: {channel.id})')

        @self.bot.command(name='log', help='Turns logging on or off\n'
                                           'Usage: !log <on|off>')
        @commands.has_permissions(administrator=True)
        async def log(ctx: commands.Context, state='') -> None:
            if state == '':
                await ctx.send('Missing Parameter; Usage: !log <on|off>')
                return
            if state == 'on':
                self.logging_active = True
            elif state == 'off':
                self.logging_active = False
            else:
                await ctx.send('Invalid parameter; Usage: !log <on|off>')
                return
            print(f'Logging: {self.logging_active}')
            await ctx.send(f'Logging: {self.logging_active}')

        @self.bot.command(name='log-file', help='Changes the file the logger writes to\n'
                                                'Usage: !log-file <filename.json> <True|False|None>')
        @commands.has_permissions(administrator=True)
        # TODO: Make create_new param here
        async def log_file(ctx: commands.Context, filename='') -> None:
            if filename == '':
                await ctx.send('Please enter a filename; !log-file <filename.json> <True|False|None>')
                return
            # Hideous solution so bot can send text message with success/failure response
            file_set = self.logger.set_log_file(filename, False)
            if file_set:
                await ctx.send('Log file has been changed successfully')
            else:
                await ctx.send('The specified file seems to not exist. Make sure you spelled the filename correctly'
                               'and ended with .json')

        @self.bot.command(name='log-create', help='Creates a file for logging\n'
                                                  'Usage: !log-create <filename.json>')
        @commands.has_permissions(administrator=True)
        async def log_create(ctx: commands.Context, filename: str = '') -> None:
            if filename == '':
                await ctx.send('Please enter a filename; !log-create <filename.json>')
                return
            elif not filename.endswith('.json'):
                await ctx.send('Filename must end with .json')
                return
            else:
                self.logger.__create_file__(filename)
                await ctx.send(
                    'Log file has been created successfully, use !log-file to change the file that is being logged to')

        @self.bot.command(name='log-out', help='Sends the current log file to the channel')
        @commands.has_permissions(administrator=True)
        async def log_out(ctx: commands.Context, filename: str = '') -> None:
            await ctx.send(
                file=discord.File(self.logger.get_log_path(), 'logfile.json' if filename == '' else filename))

    def run(self):
        self.bot.run(self.DISCORD_TOKEN)
