from mypass.config.base import Config


class ServerConfig(Config):
    CONFIG_PATH = Config.ROOT_FOLDER.joinpath('server.yaml')

    DEFAULT_HOST = 'http://localhost'
    DEFAULT_PORT = 5757

    def defaults(self):
        return {
            'host': self.DEFAULT_HOST,
            'port': self.DEFAULT_PORT,
        }
