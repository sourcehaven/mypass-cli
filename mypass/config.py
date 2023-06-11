import configparser
from pathlib import Path

import click
import rich
from mypass_logman import login, logout, session
from mypass_requests import MyPassRequests

DEFAULT_PATH = Path.home().joinpath('.mypass', 'config.ini')
DEFAULT_HOST = 'http://localhost'
DEFAULT_PORT = 5757


def write_config(host=DEFAULT_HOST, port=DEFAULT_PORT):
    DEFAULT_PATH.parent.mkdir(parents=True, exist_ok=True)

    parser = configparser.ConfigParser()
    parser['SERVER'] = {
        'host': host,
        'port': port
    }

    with open(DEFAULT_PATH, 'w') as f:
        parser.write(f)


def read_config():
    if not Path(DEFAULT_PATH).exists():
        write_config()

    parser = configparser.ConfigParser()
    parser.read(DEFAULT_PATH)

    ini_data = {}
    for section in parser.sections():
        ini_data[section] = {}
        for key, value in parser.items(section):
            ini_data[section][key] = value

    return ini_data


def login_with_prompt(*args, **kwargs):
    pw = click.prompt(text='Enter master password', hide_input=True)
    login(pw, *args, **kwargs)


def logout_with_feedback(*args, **kwargs):
    logout(*args, **kwargs)
    rich.print('[green]Logged out successfully![/green]')


def set_app(host: str, port: int):
    app = MyPassRequests()
    app.config.host = host
    app.config.port = port
    app.config.logout = logout
    app.config.login = login
    app.config.session = session
