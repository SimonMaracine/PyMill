from configparser import ConfigParser


def read_file(config: ConfigParser, file: str):
    config.read(file)
