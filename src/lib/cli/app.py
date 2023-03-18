import click
import os
import yaml
import sys
from cryptography.fernet import Fernet
from config import AppSettings, load_settings

CONTEXT_SETTINGS = dict(auto_envvar_prefix="PDA")
version: str = '0.1.0'


class Environment:
    _root_path: str | None = None
    _settings: AppSettings = None
    _config: dict[str, any] | None = None
    _fernet: Fernet | None = None

    def __init__(self):
        """ Initializes the environment. """
        self._root_path = os.getcwd()

    @property
    def root_path(self) -> str | None:
        """ Returns the path to the app's root directory. """
        return self._root_path

    @root_path.setter
    def root_path(self, value: str):
        """ Sets the app's path. """
        self._root_path = value

    @property
    def debug(self) -> bool:
        """ Returns whether debug mode is enabled. """
        return self._settings.debug if isinstance(self._settings, AppSettings) else False

    @debug.setter
    def debug(self, value: bool):
        """ Sets the debug mode. """
        if isinstance(self._settings, AppSettings):
            self._settings.debug = value

    @property
    def settings(self) -> AppSettings:
        """ Returns the app's settings. """
        return self._settings

    @settings.setter
    def settings(self, value: AppSettings):
        """ Sets the app's settings. """
        self._settings = value

    @property
    def fernet(self) -> Fernet:
        """ Returns the Fernet instance. """
        if self._fernet is None:
            self._fernet = Fernet(self._settings.secret_key)

        return self._fernet

    @staticmethod
    def log(msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.debug:
            self.log(msg, *args)


pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "cmd"))


class AsCli(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            filename = filename.lower()
            if filename.endswith('.py') and filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name: str):
        import importlib
        name = name.lower()
        try:
            mod = importlib.import_module(f'lib.cli.cmd.cmd_{name}')
        except ImportError:
            return
        return mod.cli


@click.command(cls=AsCli, context_settings=CONTEXT_SETTINGS)
@click.version_option(version, '-V', '--version', message='%(version)s')
@click.option('-p', '--root-path', type=click.Path(exists=True, file_okay=False, resolve_path=True),
              help="Overrides the application's default root path.")
@click.option("-v", "--verbose", is_flag=True, default=None, help="Increases verbosity of the application.")
@click.option('-e', '--env-file', default='.env', type=str,
              help="The path to an .env file to load command settings from.")
@click.option('--env-file-encoding', default='UTF-8', type=str,
              help="The encoding of the env file specified by the \"--env-file\" option.")
@click.option('-s', '--secrets-dir', default=None, type=str,
              help="The path to a directory containing environment variable secret files.")
@pass_environment
def cli(ctx: Environment, verbose: bool | None, root_path: str | None, env_file: str, env_file_encoding: str,
        secrets_dir: str | None):
    """A CLI to consume the app's execution and management functions."""

    if root_path is not None:
        ctx.root_path = root_path

    # Load the app's settings based on the given options.
    ctx.settings = load_settings(env_file, env_file_encoding, secrets_dir)

    # Configure the debug setting of the application if the "--verbose" option is set.
    if isinstance(verbose, bool):
        ctx.settings.debug = verbose
        ctx.debug = verbose

    # Override the root path default of the application settings if present
    if root_path is not None:
        ctx.settings.root_path = root_path
