import configparser
from pathlib import Path

from mypass_logman import signin, logout, session
from mypass_requests import MyPassRequests


DEFAULT_PATH = Path.home().joinpath('.mypass', 'config.ini')
DEFAULT_HOST = 'http://localhost'
DEFAULT_PORT = 5757


def set_config(host=DEFAULT_HOST, port=DEFAULT_PORT):
    DEFAULT_PATH.parent.mkdir(parents=True, exist_ok=True)

    parser = configparser.ConfigParser()
    parser['SERVER'] = {
        'host': host,
        'port': port
    }

    with open(DEFAULT_PATH, 'w') as f:
        parser.write(f)


def get_config():
    if not Path(DEFAULT_PATH).exists():
        set_config()

    parser = configparser.ConfigParser()
    parser.read(DEFAULT_PATH)

    ini_data = {}
    for section in parser.sections():
        ini_data[section] = {}
        for key, value in parser.items(section):
            ini_data[section][key] = value

    return ini_data


def config_app(host: str, port: int):
    app = MyPassRequests()
    app.config.host = host
    app.config.port = port
    app.config.logout = logout
    app.config.signin = signin
    app.config.session = session
    return app
