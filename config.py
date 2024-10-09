import json


class Config:

    @staticmethod
    def save(key, val):
        with open('config.json', 'r') as file_read:
            data = json.loads(file_read.read())
        data[key] = val
        with open('config.json', 'w') as file_write:
            file_write.write(json.dumps(data, indent=4))

    @staticmethod
    def load(key):
        with open('config.json', 'r') as file_read:
            data = json.loads(file_read.read())

        if key in data:
            return data[key]
        else:
            raise ConfigException("Error while reading config file", f'key {key} does not exist')

    @staticmethod
    def reset():
        with open('config.json', 'w') as file_write:
            file_write.write(json.dumps({}, indent=4))


class ConfigException(Exception):
    """Raise when a Key is not found in config.json while loading"""

    def __init__(self, message, foo, *args):
        self.message = message
        self.foo = foo
        super(ConfigException, self).__init__(message, foo, *args)
