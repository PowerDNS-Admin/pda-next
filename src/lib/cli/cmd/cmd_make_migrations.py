import click
import os
from lib.cli.app import Environment, pass_environment


@click.command("make-migrations", short_help="Run the Django makemigrations command.")
@pass_environment
def cli(ctx: Environment):
    """Run the Django makemigrations command."""

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
        ['src/manage.py', 'makemigrations']
    )
