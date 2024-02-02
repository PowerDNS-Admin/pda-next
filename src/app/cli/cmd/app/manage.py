import click
from . import group


@group.command('manage')
@click.argument('cmdargs', nargs=-1, required=True)
def wrapper(cmdargs: tuple):
    """Runs the Django management script with the given command."""
    return command(cmdargs)


def command(cmdargs: tuple) -> bool:
    """Runs the Django management script with the given command."""
    import os

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pda.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(
        ['src/manage.py', *cmdargs]
    )

    return True
