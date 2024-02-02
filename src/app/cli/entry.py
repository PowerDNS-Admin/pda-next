import os
import click
from glob import glob
from pathlib import Path
from app import settings
from app.cli import Environment

pass_environment = click.make_pass_decorator(Environment, ensure=True)


@click.group()
@click.version_option(settings.version, '-V', '--version', message='%(version)s')
@click.option('-d', '--debug', default=settings.debug, is_flag=True, help='Enables debug mode.')
@pass_environment
def cli(env: Environment, debug: bool):
    """A control interface for managing Kea-HA generated container images, networks, and containers."""

    # Update the app's settings with the CLI flag
    settings.debug = debug

    # Cache a reference to the app's settings within the environment and context.
    env.settings = settings


def import_commands():
    """ Loads all commands from the commands folder. """
    import importlib

    base_path: Path = Path(os.path.dirname(__file__))
    cmd_path: Path = base_path / 'cmd'

    for path in glob(os.path.join(cmd_path, '**/*.py'), recursive=True):
        name = os.path.basename(path)[:-3]
        relative_path = Path(path).relative_to(settings.root_path)
        import_path = '.'.join(relative_path.parts[1:])[:-3]

        if name != '__init__':
            importlib.import_module(import_path)


def confirm_option(function):
    """ A decorator that adds a confirmation prompt to the command. """
    prompt = 'Automatically answer yes to all prompts.'
    function = click.option('-y', '--yes', is_flag=True, default=False, help=prompt)(function)
    return function


def format_option(function):
    """ A decorator that adds a format option to the command. """
    meta_help = 'The output format to use. [table, json, TEMPLATE]'
    function = click.option('--format', default='table', help=meta_help)(function)
    return function


import_commands()
