import json

import discord
import pytz
from datetime import datetime


class Logger:
    _path: str

    def __init__(self, filename: str) -> None:
        self._path = 'logs/' + filename
        self.__create_file_if_not_exists__(filename)

    def __create_file_if_not_exists__(self, filename: str) -> None:
        # Try opening the specified file...
        try:
            with open(self._path, 'r') as file_read:
                print(f'Logging to file {self._path}')
        # ...and create it if not exists
        except FileNotFoundError:
            with open(self._path, 'w') as file_write:
                print(f'Creating file {self._path} to log')
                base: dict = {
                    'stats': {},
                    'messages': []
                }
                file_write.write(json.dumps(base, indent=4))

    def set_log_file(self, filename: str) -> None:
        self._path = 'logs/' + filename
        self.__create_file_if_not_exists__(filename)

    def get_log(self) -> dict:
        with open(self._path, 'r') as file_read:
            return json.load(file_read)

    def get_log_path(self) -> str:
        return self._path

    def __log_data__(self, message: str, author: str, author_id: int,
                     channel: str, channel_id: int,
                     timestamp_in_seconds: float, formatted_time: str, is_dm: bool) -> None:
        # Open log file and read data
        with open(self._path, 'r', encoding='utf-8') as file_read:
            data: dict = json.loads(file_read.read())

        # Add new entry to messages
        messages: list = data['messages']
        messages.append({
            'author': author,
            'author_id': author_id,
            'channel': channel,
            'channel_id': channel_id,
            'content': message,
            'timestamp_in_seconds': timestamp_in_seconds,
            'formatted_time': formatted_time
        })
        # if message was DM, update the message stat
        if is_dm:
            dm_count: dict = data['dm_count']
            # Add 1 to count if ID already in stats
            if str(author_id) in dm_count.keys():
                author_log = dm_count[str(author_id)]
                author_log['count'] += 1
            # Add new entry if ID not found previously
            else:
                dm_count[str(author_id)] = {
                    'name': author,
                    'count': 1
                }
        # TODO Logging for all text channels to gather insights?!
        with open(self._path, 'w') as file_write:
            file_write.write(json.dumps(data, indent=4))

    def __prep_data__(self, message: discord.Message, is_dm: bool) -> dict:
        """
        Prepares the data to be logged and then calls the log method with prepared data
        :param message: The message to be prepared
        :param is_dm: States if the message is a DM
        :return: None
        """
        channel: str = message.author.name + '_dm' if is_dm else message.channel.name
        formatted_time: str = message.created_at.strftime('%d.%m.%Y %H:%M')
        zoned_date: datetime = message.created_at.astimezone(pytz.timezone('Europe/Berlin'))
        formatted_time: str = zoned_date.strftime('%d.%m.%Y %H:%M')

        # TODO Refactor to use log_dm and log_text_channel
        prepped_data = {
            "content": message.content,
            "author": message.author.name,
            "author_id": message.author.id,
            "channel": channel,
            "channel_id": message.channel.id,
            "timestamp": message.created_at.timestamp(),
            "formatted_time": formatted_time
        }
        return prepped_data

    def log_dm(self, message: discord.Message) -> None:
        prepped_data = self.__prep_data__(message, True)
        self.__log_data__(prepped_data['content'], prepped_data['author'],
                          prepped_data['author_id'], prepped_data['channel'],
                          prepped_data['channel_id'], prepped_data['timestamp'],
                          prepped_data['formatted_time'], True)

