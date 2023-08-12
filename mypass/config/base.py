from abc import abstractmethod, ABC
from pathlib import Path
from typing import Any

from mypass.util.fs import create_paths, write_yaml_missing_keys, write_yaml, update_yaml, read_yaml


class Config(ABC):
    ROOT_FOLDER = Path.home().joinpath('.mypass')
    CONFIG_PATH = None

    def __init__(self, *paths: Path):
        create_paths(self.ROOT_FOLDER, self.CONFIG_PATH, *paths)
        write_yaml_missing_keys(self.CONFIG_PATH, self.defaults())

    @abstractmethod
    def defaults(self) -> dict[str, Any]:
        ...

    def set_default(self):
        write_yaml(self.CONFIG_PATH, self.defaults())

    def update(self, key: str, value):
        update_yaml(self.CONFIG_PATH, key, value)

    def read(self, key: str = None):
        data = read_yaml(self.CONFIG_PATH)
        if key is None:
            return data

        return data[key]

