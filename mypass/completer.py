from typing import Iterable

from prompt_toolkit.completion import Completer, CompleteEvent, Completion, NestedCompleter
from prompt_toolkit.document import Document


def find_reverse_substring_index(text: str, word: str):
    word_len = len(word)
    for i in range(word_len):
        sub_word = word[:word_len - i]
        index = text.rfind(sub_word)
        if index != -1:
            return index - len(text)
    return 0


class SequenceCompleter(Completer):

    def __init__(self, *options: str | tuple[str, ...]):
        self.options = tuple((option,) if isinstance(option, str) else option for option in options)

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        text_lower = document.text_before_cursor.lower()

        for option in self.options:
            if any(word.lower() in text_lower for word in option):
                continue
            else:
                for word in option:
                    start_position = find_reverse_substring_index(text_lower, word.lower())
                    yield Completion(text=word, start_position=start_position)
                break


def get_completer():
    vault_completer = NestedCompleter.from_nested_dict({
        'add': None,
        'read': None,
        'copy': None,
        'list': None,
        'update': None,
        'delete': None
    })

    master_completer = NestedCompleter.from_nested_dict({
        'update': None,
    })

    return NestedCompleter.from_nested_dict({
        'vault': vault_completer,
        'master': master_completer,
        'sql': {
            'SELECT': SequenceCompleter('FROM', 'WHERE'),
            'INSERT': SequenceCompleter('VALUES'),
            'UPDATE': SequenceCompleter('SET', 'WHERE'),
            'DELETE': SequenceCompleter('WHERE'),
            'TRUNCATE': None,
        },
        'help': {
            'vault': None,
            'master': None,
            'sql': None,
            'exit': None,
            'quit': None,
        },
        'exit': None,
        'quit': None,
    })
