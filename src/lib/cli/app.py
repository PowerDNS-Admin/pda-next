import click
import os
import yaml
import sys
from cryptography.fernet import Fernet
from config import AppSettings

CONTEXT_SETTINGS = dict(auto_envvar_prefix="PDA")
version: str = '0.1.0'


class Environment:
    _app_path: str | None = None
    _settings: AppSettings = None
    _config: dict[str, any] | None = None
    _fernet: Fernet | None = None

    def __init__(self):
        """ Initializes the environment. """
        self._app_path = os.getcwd()

    @property
    def app_path(self) -> str | None:
        """ Returns the path to the app's root directory. """
        return self._app_path

    @app_path.setter
    def app_path(self, value: str):
        """ Sets the app's path. """
        self._app_path = value

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

    @property
    def config(self) -> dict[str, any]:
        """ Returns the app's configuration. """
        return self._config

    @property
    def fernet(self) -> Fernet:
        """ Returns the Fernet instance. """
        if self._fernet is None:
            self._fernet = Fernet(self._settings.secret_key)

        return self._fernet

    def load_settings(self, env_file: str, env_file_encoding: str, secrets_dir: str | None) -> AppSettings:
        """ Loads the app's settings from the given environment file and secrets directory. """

        if not env_file.startswith('/'):
            env_file = os.path.join(self.app_path, env_file)

        params: dict = {
            '_env_file': env_file,
            '_env_file_encoding': env_file_encoding,
        }

        os.putenv('PDA_ENV_FILE', env_file)
        os.putenv('PDA_ENV_FILE_ENCODING', env_file_encoding)

        if secrets_dir is not None:
            valid: bool = True
            secrets_path: str = secrets_dir if secrets_dir.startswith('/') else os.path.join(self.app_path,
                                                                                             secrets_dir)

            if not os.path.exists(secrets_path):
                valid = False
                self.log(f'The given path for the "--secrets-dir" option does not exist: {secrets_path}')
            elif not os.path.isdir(secrets_path):
                valid = False
                self.log(f'The given path for the "--secrets-dir" option is not a directory: {secrets_path}')

            if valid:
                params['_secrets_dir'] = secrets_dir
                os.putenv('PDA_ENV_SECRETS_DIR', secrets_dir)

        self._settings: AppSettings = AppSettings(**params)

        return self._settings

    def load_config(self):
        """ Loads the app's configuration from the given configuration file. """

        if self._settings is None:
            raise Exception('The app settings have not been loaded yet.')

        if self._config is not None:
            return self._config

        config_path: str = self._settings.config

        if not config_path.startswith('/'):
            config_path = os.path.join(self.app_path, config_path)

        if not os.path.exists(config_path):
            raise Exception(f'The given path for the configuration file does not exist: {config_path}')

        if not os.path.isfile(config_path):
            raise Exception(f'The given path for the configuration file is not a file: {config_path}')

        with open(config_path, 'r') as f:
            self._config = yaml.load(f, Loader=yaml.FullLoader)
            f.close()

    def save_config(self, config: dict[str, any]) -> bool:
        """ Saves the app's configuration to the given configuration file. """

        if self._settings is None:
            raise Exception('The app settings have not been loaded yet.')

        config_path: str = self._settings.config

        if not config_path.startswith('/'):
            config_path = os.path.join(self.app_path, config_path)

        with open(config_path, 'w') as f:
            yaml.dump(config, f)
            f.close()

        return True

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
@click.option('-p', '--app-path', type=click.Path(exists=True, file_okay=False, resolve_path=True),
              help="Changes the app's root path.")
@click.option("-v", "--verbose", is_flag=True, default=None, help="Increases verbosity of the application.")
@click.option('-e', '--env-file', default='.env', type=str,
              help="The path to an .env file to load command settings from.")
@click.option('--env-file-encoding', default='UTF-8', type=str,
              help="The encoding of the env file specified by the \"--env-file\" option.")
@click.option('-s', '--secrets-dir', default=None, type=str,
              help="The path to a directory containing environment variable secret files.")
@pass_environment
def cli(ctx: Environment, verbose: bool | None, app_path: str | None, env_file: str, env_file_encoding: str,
        secrets_dir: str | None):
    """A CLI to consume the app's execution and management functions."""

    # Configure the debug setting of the application if the "--verbose" option is set.
    if isinstance(verbose, bool):
        ctx.debug = verbose

    # Cache a reference to the app's root path
    if app_path is not None:
        ctx.app_path = app_path

    # Load the app's settings based on the given options.
    ctx.load_settings(env_file, env_file_encoding, secrets_dir)

    # Load the app's configuration based on the given settings.
    ctx.load_config()
