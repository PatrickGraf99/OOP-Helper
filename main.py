import os

import discord
from discord.ext import commands



class OOPBot:
    def __init__(self):

        self.DISCORD_TOKEN: str = 'Place token here'

        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix='!', intents=intents)

        self.dm_channel_id = -99
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
                await target_channel.send(f'Forwarded Message:\n{message.content}')
            await self.bot.process_commands(message)

    def __register_commands__(self) -> None:

        @self.bot.command(name='dm-channel', help='Sets the channel where bot DMs will be redirected to\n'
                                                  'Usage: !dm-channel <channel_id>')
        @commands.has_permissions(administrator=True)
        async def dm_channel(ctx: commands.Context, channel_id=-99) -> None:
            if type(channel_id) is not int:
                await ctx.send('Please enter a valid channel id; !dm-channel <channel_id>')
                return
            if channel_id == -99:
                await ctx.send('Please enter a valid channel id; !dm-channel <channel_id>')
                return
            guild: discord.Guild = ctx.guild
            # TODO Use category in combination with channel name to uniquely identify the channel
            channel: discord.TextChannel = discord.utils.get(guild.text_channels, id=channel_id)
            if channel is None:
                await ctx.send(f'Sorry, I couldn\'t find the channel with id \"{channel_id}\"')
                return
            self.dm_channel_id = channel.id
            await ctx.send(f'All DMs the bot receives will be redirected to {channel.mention} (ID: {channel.id})')

    def run(self):
        self.bot.run(self.DISCORD_TOKEN)


if __name__ == '__main__':
    bot = OOPBot()
    bot.run()
