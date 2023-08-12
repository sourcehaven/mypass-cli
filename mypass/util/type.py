from mypass.exception import InvalidValue


def convert_to_bool(key: str, val: str):
    try:
        val = int(val)
        if val == 0:
            return False
        return True
    except ValueError:
        val = val.lower()
        if val in ['false', 'off', 'disable', 'no', 'n']:
            return False
        if val in ['true', 'on', 'enable', 'yes', 'y']:
            return True
        raise InvalidValue(f"Entered value {val!r} for {key!r} is not a known on/off flag!")
