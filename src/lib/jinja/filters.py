
def action_label(value: int):
    return 'Update' if value else 'Create'


def no_value(value):
    return '' if value is None else value


def none_value(value):
    return 'None' if value is None or not len(str(value).strip()) else value


def selected(value, match):
    return 'selected' if value == match else ''


def checked(value, match):
    return 'checked' if value == match else ''


def format_phone(value):
    formatted: str = str(value)
    length: int = len(value)

    if length == 7:
        formatted = f'{value[:3]}-{value[3:]}'
    elif length == 10:
        formatted = f'({value[:3]}) {value[3:6]}-{value[6:]}'
    elif length == 11:
        formatted = f'{value[:1]} ({value[1:4]}) {value[4:7]}-{value[7:]}'
    elif length == 12:
        formatted = f'{value[:2]} ({value[2:5]}) {value[5:8]}-{value[8:]}'
    elif length == 13:
        formatted = f'{value[:3]} ({value[3:6]}) {value[6:9]}-{value[9:]}'

    return formatted
