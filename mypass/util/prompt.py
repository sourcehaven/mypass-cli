from typing import Callable

from prompt_toolkit.shortcuts import input_dialog

from mypass.exception import PasswordError


def password_dialog(description: str, hide_text=True):
    return input_dialog(
        title="Password prompt",
        text=description,
        password=hide_text,
    ).run()


def default_validator(pw: str):
    if pw:
        return len(pw) > 3
    return False


def new_master_password_dialog(validator: Callable[[str], bool] = default_validator, hide_text=True):
    new_pw = password_dialog('Enter new master password:', hide_text=hide_text)

    # If password dialog is not cancelled.
    if new_pw is not None:
        if validator(new_pw):
            re_new_pw = password_dialog('Confirm new master password:', hide_text=hide_text)
            if new_pw == re_new_pw:
                return new_pw
            else:
                raise PasswordError.password_do_not_match()
        else:
            raise PasswordError.weak_password()
    else:
        raise PasswordError.operation_cancelled()


def update_master_password_dialog(current_password: str, new_validator: Callable[[str], bool] = default_validator, hide_text=True):
    pw = password_dialog('Enter master password:', hide_text=hide_text)

    if pw is not None:
        if pw == current_password:
            return new_master_password_dialog(new_validator, hide_text=hide_text)
        else:
            raise PasswordError.incorrect_password()
    else:
        raise PasswordError.operation_cancelled()
