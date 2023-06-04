import click
from click_shell import shell

from rich.console import Console
from rich.text import Text

console = Console()


@shell(
    prompt='mypass > ',
    intro='Welcome to MyPass CLI. To get started type "help".'
)
def mypass():
    """MyPass - Password Manager CLI"""
    pass


@mypass.command()
@click.argument('name', type=str, required=True)
@click.option('--email', '-e', type=str, help='Email for the entry.')
@click.option('--username', '-u', type=str, help='Username for the entry.')
@click.option('--password', '-p', type=str, help='Password for the entry.')
@click.option('--prompt-password', '-pp', is_flag=True, help='Secure prompt to enter password.')
@click.option('--length', '-l', type=int, default=12, help='Password length.')
@click.option('--site', '-s', type=str, help='Site for the entry.')
def add(name: str, email: str, username: str, password: str, prompt_password: bool, length: int, site: str):
    if prompt_password and password is not None:
        raise click.ClickException('--password must not be used along with --prompt-password flag')

    if prompt_password:
        password = click.prompt('Enter your password: ', hide_input=True, confirmation_prompt=False)

    """Add an entry to the password store"""
    click.echo(f"Adding entry: {name}")
    click.echo(f"Email: {email}")
    click.echo(f"Username: {username}")
    click.echo(f"Password: {password}")
    click.echo(f"Password prompt: {prompt_password}")
    click.echo(f"Password length: {length}")
    click.echo(f"Site: {site}")


@mypass.command()
@click.argument('name', nargs=-1)
def delete(name):
    """Remove an entry from the password store"""
    if not name:
        error_text = Text("Please provide at least one entry name to delete", style="bold red")
        console.print(error_text)
        raise click.Abort()
    click.echo(f"Deleting entry: {', '.join(name)}")


@mypass.command()
@click.argument('name', nargs=-1)
def show(name):
    """Show entries from the password store"""
    if name:
        click.echo(f"Showing entry: {', '.join(name)}")
    else:
        click.echo("Showing all entries")


@mypass.command()
@click.option('--all', '-a', is_flag=True, help='Copy all credentials')
@click.option('--email', '-e', is_flag=True, help='Copy email')
@click.option('--username', '-u', is_flag=True, help='Copy username')
@click.option('--password', '-p', is_flag=True, help='Copy password')
@click.option('--site', '-s', is_flag=True, help='Copy site')
def copy(all, email, username, password, site):
    """Copy entry credentials to the clipboard"""
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


@mypass.command()
@click.argument('name', type=str, required=True)
@click.option('--email', '-e', type=str, help='Change email')
@click.option('--username', '-u', type=str, help='Change username')
@click.option('--password', '-p', type=str, help='Change password')
@click.option('--site', '-s', type=str, help='Change site')
def change(name, email, username, password, site):
    """Change password manager entry"""
    click.echo(f"Changing entry: {name}")
    click.echo(f"Email: {email}")
    click.echo(f"Username: {username}")
    click.echo(f"Password: {password}")
    click.echo(f"Site: {site}")
