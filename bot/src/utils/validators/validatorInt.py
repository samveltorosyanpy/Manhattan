def is_valid_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False