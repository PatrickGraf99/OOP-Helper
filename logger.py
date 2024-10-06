import json


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

    def set_log_file(self, filename: str):
        self._path = 'logs/' + filename
        self.__create_file_if_not_exists__(filename)

    def get_log(self) -> dict:
        with open(self._path, 'r') as file_read:
            return json.load(file_read)

    def log(self, message: str, author: str, timestamp_in_seconds: float, formatted_time: str) -> None:
        # Open log file and read data
        with open(self._path, 'r', encoding='utf-8') as file_read:
            data: dict = json.loads(file_read.read())
            print('File contents: ' + file_read.read())

        # Add new entry to data
        messages: list = data['messages']
        messages.append({
            'author': author,
            'content': message,
            'timestamp_in_seconds': timestamp_in_seconds,
            'formatted_time': formatted_time
        })
        dm_count: dict = data['dm_count']
        if author in dm_count.keys():
            dm_count[author] += 1
        else:
            dm_count[author] = 1

        with open(self._path, 'w') as file_write:
            file_write.write(json.dumps(data, indent=4))


logger = Logger('log.json')
logger.log("hi", "günni", 1, "-")
