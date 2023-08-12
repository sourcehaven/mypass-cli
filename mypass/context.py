from mypass.config.cli import CliConfig
from mypass.config.server import ServerConfig


class AppContext:

    def __init__(self, server: ServerConfig, cli: CliConfig):
        self.server = server
        self.cli = cli

    @property
    def welcome(self):
        return self.cli.read('welcome')

    @welcome.setter
    def welcome(self, value: bool):
        self.cli.update('welcome', value)

    @property
    def history(self):
        return self.cli.read('history')

    @history.setter
    def history(self, value: bool):
        self.cli.update('history', value)

    @property
    def host(self):
        return self.server.read('host')

    @host.setter
    def host(self, value: str):
        self.server.update('host', value)

    @property
    def port(self):
        return self.server.read('port')

    @port.setter
    def port(self, value: int):
        self.server.update('port', value)
