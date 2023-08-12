from pathlib import Path
from typing import Any

import yaml


def create_paths(*paths: Path):

    folders = (path for path in paths if not path.suffix)
    files = (path for path in paths if path.suffix)

    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)

    for file in files:
        if not file.exists():
            file.touch()


def read_yaml(path: Path):
    with open(path, 'r') as stream:
        return yaml.safe_load(stream)


def write_yaml(path: Path, data: dict[str, Any]):
    with open(path, 'w') as f:
        yaml.safe_dump(data, f)


def write_yaml_missing_keys(path: Path, defaults: dict[str, Any]):
    data = read_yaml(path)

    if data is None:
        data = {}

    for key, val in defaults.items():
        if key not in data:
            data[key] = val

    write_yaml(path, data)


def update_yaml(path: Path, key: str, value):
    data = read_yaml(path)
    data[key] = value
    write_yaml(path, data)
