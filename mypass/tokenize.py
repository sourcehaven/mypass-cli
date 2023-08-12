import re
from tokenize import Token

from mypass_tokens.command.tokens import command_tokens
from mypass_tokens.git.tokens import GitCommand
from mypass_tokens.sql.tokens import Select, Truncate, Update, Delete, Insert, SqlCommand

from mypass_tokens.command.tokenizer import tokenize as tokenize_command
from mypass_tokens.git.tokenizer import tokenize as tokenize_git
from mypass_tokens.sql.tokenizer import tokenize as tokenize_sql
from mypass_tokens.tokens import Unknown


def make_pattern(*tokens: Token):
    return re.compile(r'^\s*' + '|'.join(token.pattern.pattern for token in tokens), re.I)


def tokenize(text: str, remove_spaces=False):
    git_pattern = make_pattern(GitCommand)
    sql_pattern = make_pattern(SqlCommand, Select, Insert, Update, Delete, Truncate)
    command_pattern = make_pattern(*command_tokens)

    if re.match(sql_pattern, text):
        return 'sql', tokenize_sql(text, remove_spaces)
    if re.match(git_pattern, text):
        return 'git', tokenize_git(text, remove_spaces)
    if re.match(command_pattern, text):
        return 'command', tokenize_command(text, remove_spaces)
    return 'unknown', [Unknown(text, 0, len(text), 1)]
