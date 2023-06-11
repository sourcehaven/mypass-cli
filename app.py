from argparse import ArgumentParser
from typing import Union

from mypass.cli import mypass
from mypass.config import write_config, read_config, set_app


def run(host: Union[str, None], port: Union[int, None]):
    if host is None or port is None:
        conf = read_config()

        if host is None:
            host = conf['SERVER']['host']
        if port is None:
            port = int(conf['SERVER']['port'])

    write_config(host=host, port=port)
    set_app(host=host, port=port)

    mypass()


if __name__ == '__main__':
    arg_parser = ArgumentParser('MyPass')
    arg_parser.add_argument(
        '-H', '--host', type=str, default=None,
        help=f'Specifies the server host.')
    arg_parser.add_argument(
        '-p', '--port', type=int, default=None,
        help=f'Specifies the server port.')

    args = arg_parser.parse_args()

    run(host=args.host, port=args.port)
