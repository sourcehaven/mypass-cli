from typing import Sequence

from prompt_toolkit import PromptSession, print_formatted_text as print, HTML
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard

from mypass_tokens.command.tokens import Quit, Help, History, Port, Host, Clear, Vault, Master, primary_keywords as primary_command_keywords
from mypass_tokens.git.tokens import primary_keywords as primary_git_keywords
from mypass_tokens.sql.tokens import primary_keywords as primary_sql_keywords
from mypass_tokens.tokens import Token

from mypass.completer import get_completer
from mypass.config.cli import CliConfig
from mypass.config.server import ServerConfig
from mypass.context import AppContext
from mypass.lexer import CliLexer
from mypass.tokenize import tokenize
from mypass.util.console import clear_screen
from mypass.util.help import suggest_correction


def bottom_toolbar():
    return [(
        'class:bottom-toolbar',
        'Press ctr-d or ctr-c to exit'
    )]


def input_processor(mode, tokens: Sequence[Token], inp: str, app_context: AppContext):
    if mode == 'command':
        match tokens[0]:
            case Vault():
                print('Vault command!')
            case Master():
                print('Master command!')
            case Quit():
                raise KeyboardInterrupt
            case Help():
                print('Help!')
            case History():
                for dtm, value in app_context.cli.read_history():
                    print(HTML(f'<ansigreen>{dtm}</ansigreen>'), value)
            case Port():
                print(app_context.port)
            case Host():
                print(app_context.host)
            case Clear():
                clear_screen()
            case _:
                raise NotImplementedError
    elif mode == 'sql':
        ...
    elif mode == 'git':
        ...
    elif mode == 'unknown':
        print(HTML(suggest_correction(
            tokens[0].value,
            (*primary_command_keywords, *primary_git_keywords, *primary_sql_keywords)
        )))


def main(context: AppContext):
    style = Style.from_dict({
        'bottom-toolbar': '#333333 bg:#ffcc00'
    })

    if context.welcome:
        print("""Welcome to MyPass CLI.

Enter "setup" to personalize your environment.
Enter "help" to see available commands.
Enter "welcome: off" if you do not wish to see this welcome (Enter "welcome: on" to re-enable)
""")

    lexer = CliLexer()
    session = PromptSession(
        history=FileHistory(context.cli.HISTORY_PATH) if context.history else None,
        # enable_history_search=True, # this breaks the completer
        auto_suggest=AutoSuggestFromHistory(),
        clipboard=PyperclipClipboard(),
        style=style,
        lexer=lexer,
        completer=get_completer(),
        bottom_toolbar=bottom_toolbar,
    )

    while True:
        try:
            text: str = session.prompt('mypass > ', rprompt=lambda: f'mode: {lexer.mode}')

            mode, tokens = tokenize(text)
            input_processor(mode, tokens, text, app_context)

        # ctrl+c, ctrl+d
        except (EOFError, KeyboardInterrupt):
            break


if __name__ == '__main__':
    app_context = AppContext(ServerConfig(), CliConfig())
    main(app_context)
