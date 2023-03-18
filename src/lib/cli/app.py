import click
import os
import sys
from cryptography.fernet import Fernet
from config import AppSettings, settings

CONTEXT_SETTINGS = dict(auto_envvar_prefix="PDA")
version: str = settings.version


class Environment:
    _settings: AppSettings = None
    _fernet: Fernet | None = None

    @property
    def debug(self) -> bool:
        """ Returns whether debug mode is enabled. """
        return self._settings.debug if isinstance(self._settings, AppSettings) else False

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
@pass_environment
def cli(ctx: Environment):
    """A CLI to consume the app's execution and management functions."""

    # Cache a reference to the app's settings within the context.
    ctx.settings = settings
