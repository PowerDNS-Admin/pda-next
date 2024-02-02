import click
from app.cli import Environment
from app.cli.entry import pass_environment, format_option
from . import group

meta_help: dict = {
    'flat': 'Flattens the JSON output to a single line.',
}


@group.command('show')
@format_option
@click.option('--flat', is_flag=True, default=False, help=meta_help['flat'])
@click.argument('key', required=False, default=None, metavar='<KEY>')
@pass_environment
def wrapper(env: Environment, format: str, flat: bool, key: str = None):
    """Shows the current environment configuration in multiple formats, with optional formatting."""
    return command(env, format, flat, key)


def command(env: Environment, format: str, flat: bool = True, key: str = None) -> bool:
    """Shows the current environment configuration in multiple formats, with optional formatting."""

    ref = env.config

    if key:
        ref = env.config[key]

    if format == 'json':
        click.echo(ref().to_json(flat=flat))
    elif format == 'yaml':
        click.echo(ref().yaml)
    else:
        click.echo(ref)

    return True
