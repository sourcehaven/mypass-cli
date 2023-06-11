import configparser
import webbrowser

import click
from click_shell import shell

import rich
from rich.console import Console
from rich.text import Text

from mypass_requests import update_master_pw

from mypass.config import DEFAULT_PATH
from mypass.util import clear_screen

console = Console()


@shell(
    prompt='mypass > ',
    intro='Welcome to MyPass CLI. To get started type "help".'
)
def mypass():
    """MyPass - Password Manager CLI"""
    pass

# ---------------------------------------------------  Common  ----------------------------------------------------- #


@mypass.command()
def cls():
    """Clears screen. Alias for "clear" command."""
    clear_screen()


@mypass.command()
def clear():
    """Clears screen. Alias for "cls" command."""
    clear_screen()

# ----------------------------------------------------  Vault  ----------------------------------------------------- #


@mypass.group()
def vault():
    """Contains commands for vault operations."""
    pass


@vault.command()
@click.argument('name', type=str, required=True)
@click.option('--email', '-e', type=str, help='Email for the entry.')
@click.option('--username', '-u', type=str, help='Username for the entry.')
@click.option('--password', '-p', type=str, help='Password for the entry.')
@click.option('--prompt-password', '-pp', type=bool, is_flag=True, help='Secure prompt for password.')
@click.option('--site', '-s', type=str, help='Site for the entry.')
def add(name: str, email: str, username: str, password: str, prompt_password: bool, site: str):
    """Add an entry to the password vault."""

    if prompt_password and password is not None:
        raise click.ClickException('--password must not be used along with --prompt-password flag')

    if prompt_password:
        password = click.prompt('Enter your password', hide_input=True)

    click.echo(f"Adding entry: {name}")
    click.echo(f"Email: {email}")
    click.echo(f"Username: {username}")
    click.echo(f"Password: {password}")
    click.echo(f"Password prompt: {prompt_password}")
    click.echo(f"Site: {site}")


@vault.command()
@click.argument('name', type=str, required=True)
@click.option('--email', '-e', type=str, help='Email for the entry.')
@click.option('--username', '-u', type=str, help='Username for the entry.')
@click.option('--site', '-s', type=str, help='Site for the entry.')
@click.option('--length', '-l', type=int, default=12, help='Generated password length.')
@click.option('--special', is_flag=True, default=True, help='Include special characters.')
def generate(name: str, email: str, username: str, site: str, length: int, special: bool):
    """
    Add an entry to the password vault with auto generated password.

    Copies generated password to clipboard.
    """

    click.echo(f"Adding entry: {name}")
    click.echo(f"Email: {email}")
    click.echo(f"Username: {username}")
    click.echo(f"Password length: {length}")
    click.echo(f"Site: {site}")
    click.echo(f"Special: {special}")


@vault.command()
@click.argument('name', type=str, nargs=-1)
def delete(name):
    """Remove an entry from the password vault."""
    if not name:
        error_text = Text("Please provide at least one entry name to delete", style="bold red")
        rich.print(error_text)
        raise click.Abort()
    click.echo(f"Deleting entry: {', '.join(name)}")


@vault.command()
@click.argument('name', type=str, nargs=-1)
def show(name: str):
    """Show entries from the password vault."""
    if name:
        click.echo(f"Showing entry: {', '.join(name)}")
    else:
        click.echo("Showing all entries")


@vault.command()
@click.option('--all', '-a', is_flag=True, help='Copy all credentials')
@click.option('--email', '-e', is_flag=True, help='Copy email')
@click.option('--username', '-u', is_flag=True, help='Copy username')
@click.option('--password', '-p', is_flag=True, help='Copy password')
@click.option('--site', '-s', is_flag=True, help='Copy site')
def copy(all: bool, email: bool, username: bool, password: bool, site: bool):
    """Copy entry credentials to the clipboard."""
    if all:
        click.echo("Copying all credentials")
    elif email:
        click.echo("Copying email")
    elif username:
        click.echo("Copying username")
    elif password:
        click.echo("Copying password")
    elif site:
        click.echo("Copying site")
    else:
        click.echo("No option specified")


@vault.command()
@click.argument('name', type=str, required=True)
@click.option('--email', '-e', type=str, help='Change email')
@click.option('--username', '-u', type=str, help='Change username')
@click.option('--password', '-p', type=str, help='Change password')
@click.option('--site', '-s', type=str, help='Change site')
def change(name: str, email: str, username: str, password: str, site: str):
    """Change password manager entry."""
    click.echo(f"Changing entry: {name}")
    click.echo(f"Email: {email}")
    click.echo(f"Username: {username}")
    click.echo(f"Password: {password}")
    click.echo(f"Site: {site}")

# ----------------------------------------------------  Master ----------------------------------------------------- #


@mypass.group()
def master():
    """Contains commands for master password operations."""
    pass


@master.command()
def update():
    inp_new_mpass = click.prompt(
        text='Enter new master password', hide_input=True, confirmation_prompt='Confirm new master password')

    update_master_pw(pw=inp_new_mpass)
    rich.print('[green]Master password successfully updated![/green]')


# ----------------------------------------------------  Config ----------------------------------------------------- #


@mypass.group()
def config():
    """Contains commands for config operations."""
    pass


@config.command()
@click.option('--host', '-h', is_flag=True, default=False, help='Print server host.')
@click.option('--port', '-p', is_flag=True, default=False, help='Print server port.')
def show(host: bool, port: bool):
    """Display config settings."""
    if not host and not port:
        with open(DEFAULT_PATH, 'r') as file:
            config_contents = file.read()
            rich.print(config_contents.strip())
    else:
        parser = configparser.ConfigParser()
        parser.read(DEFAULT_PATH)
        if host:
            rich.print('Host=', parser.get('SERVER', 'host'), sep='')
        if port:
            rich.print('Port=', parser.get('SERVER', 'port'), sep='')


@config.command()
@click.option('--host', '-h', type=str, help='Set server host.')
@click.option('--port', '-p', type=int, help='Set server port.')
def update(host: str, port: int):
    """Set config settings."""
    if host is None and port is None:
        webbrowser.open(str(DEFAULT_PATH))
    else:
        parser = configparser.ConfigParser()
        parser.read(DEFAULT_PATH)

        if host is not None:
            parser.set('SERVER', 'host', host)
            rich.print(f'SERVER.host changed to: {host}')
        if port is not None:
            parser.set('SERVER', 'port', str(port))
            rich.print(f'SERVER.port changed to: {port}')

        with open(DEFAULT_PATH, 'w') as f:
            parser.write(f)
