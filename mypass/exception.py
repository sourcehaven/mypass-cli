class InvalidValue(Exception):

    def __init__(self, msg: str):
        super().__init__('Invalid value: ', msg)


class PasswordError(Exception):

    @classmethod
    def weak_password(cls, min_requirements: str = None):
        err_msg = 'Entered password is too weak!'

        if min_requirements:
            err_msg += f' {min_requirements}'

        return cls(err_msg)

    @classmethod
    def incorrect_password(cls):
        return cls('Entered password is incorrect!')

    @classmethod
    def operation_cancelled(cls):
        return cls('Operation was interrupted!')

    @classmethod
    def password_do_not_match(cls):
        return cls('Confirm password does not match!')

    def __init__(self, msg: str):
        super().__init__(msg)
