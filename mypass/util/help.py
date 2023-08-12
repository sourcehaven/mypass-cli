import difflib
from typing import Iterable


def suggest_correction(user_input: str, valid_commands: Iterable[str]):
    closest_match = difflib.get_close_matches(user_input, valid_commands, n=1)

    if closest_match:
        err = f"Unknown command '{user_input}', did you mean '{closest_match[0]}'?"
    else:
        err = f"Unknown command '{user_input}'. Type 'help' to see available commands."

    return f'<ansired>{err}</ansired>'
