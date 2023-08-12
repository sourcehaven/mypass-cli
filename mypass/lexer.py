from prompt_toolkit.lexers import Lexer

from mypass.tokenize import tokenize


from prompt_toolkit.styles import ANSI_COLOR_NAMES
class CliLexer(Lexer):

    def __init__(self):
        self.mode = 'unknown'

    def lex_document(self, document):

        def get_line(lineno):
            text = document.lines[lineno]
            mode, tokens = tokenize(text)
            self.mode = mode

            return [(token.color, token.value) for token in tokens]

        return get_line
