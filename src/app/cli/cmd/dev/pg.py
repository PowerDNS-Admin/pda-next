import click
from app.cli import Environment
from app.cli.entry import pass_environment
from . import group


@group.command('pg')
@click.argument('key', required=False, default=None, metavar='<KEY>')
@pass_environment
def wrapper(env: Environment, key: str = None):
    """Provides a development playground for quickly testing code."""
    return command(env, key)


def command(env: Environment, key: str = None) -> bool:
    """Provides a development playground for quickly testing code."""
    return True
