from datetime import datetime

from mypass.config.base import Config


class CliConfig(Config):
    DIR = Config.ROOT_FOLDER.joinpath('cli')
    CONFIG_PATH = DIR.joinpath('config.yaml')
    HISTORY_PATH = DIR.joinpath('history.txt')

    DEFAULT_WELCOME = True
    DEFAULT_HISTORY = True

    def __init__(self):
        super().__init__(self.DIR, self.HISTORY_PATH)

    def defaults(self):
        return {
            'welcome': self.DEFAULT_WELCOME,
            'history': self.DEFAULT_HISTORY,
        }

    def clear_history(self):
        try:
            with open(self.HISTORY_PATH, 'w') as hist:
                hist.truncate(0)
        except FileNotFoundError:
            pass

    def read_history(self, start_date: str | datetime = None, end_date: str | datetime = None):
        date_format = "%Y-%m-%d %H:%M:%S.%f"

        if start_date and isinstance(start_date, str):
            start_date = datetime.strptime(start_date, date_format)
        if end_date and isinstance(end_date, str):
            end_date = datetime.strptime(end_date, date_format)

        with open(self.HISTORY_PATH, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    timestamp = datetime.strptime(line.replace('#', '').strip(), date_format)
                    if (start_date is None or start_date <= timestamp) and (end_date is None or timestamp <= end_date):
                        yield timestamp, next(f).replace('+', '').strip()
