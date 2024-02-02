import os
from pathlib import Path
from reflective import Reflective
from app.model.settings import AppSettings
from app.util.config import ConfigLoader

ROOT_PATH: Path = Path(os.getcwd())
""" The root path of the application which is typically the project repository root directory."""

DEFAULT_CONFIG_PATH: Path = ROOT_PATH / 'defaults.yml'
""" The file containing the default YAML configuration to use when an environment specific file is missing. """

DEFAULT_ENV_PATH: Path = ROOT_PATH / '.env'
""" The default path to the environment file to load settings from. """

DEFAULT_ENV_FILE_ENCODING: str = 'UTF-8'
""" The default file encoding of the environment file to load settings from. """

DEFAULT_SECRETS_PATH: Path or None = None
""" The default path to the secrets directory to load environment variable values from. """


def load_settings(env_prefix: str) -> AppSettings:
    """ Loads an AppSettings instance based on the given environment file and secrets directory. """
    from loguru import logger

    # Extract the default environment file path from the environment if defined, otherwise use the default path
    env_file_path = os.getenv(f'{env_prefix}_ENV_FILE', DEFAULT_ENV_PATH)

    # Extract the default environment file encoding from the environment if defined, otherwise use the default value
    env_file_encoding = os.getenv(f'{env_prefix}_ENV_FILE_ENCODING', DEFAULT_ENV_FILE_ENCODING)

    # Extract the default secrets directory path from the environment if defined, otherwise use the default path
    secrets_path = os.getenv(f'{env_prefix}_ENV_SECRETS_DIR', DEFAULT_SECRETS_PATH)

    if env_file_path is not None and not isinstance(env_file_path, Path):
        env_file_path = Path(env_file_path)

    if secrets_path is not None and not isinstance(secrets_path, Path):
        secrets_path = Path(secrets_path)

    params: dict = {
        'root_path': str(ROOT_PATH),
        'env_file': str(env_file_path),
        'env_file_encoding': env_file_encoding,
        '_env_file': env_file_path,
        '_env_file_encoding': env_file_encoding,
    }

    # Ensure any default values get pushed back into the environment
    os.putenv(f'{env_prefix}_ENV_FILE', str(env_file_path))
    os.putenv(f'{env_prefix}_ENV_FILE_ENCODING', env_file_encoding)

    if secrets_path is not None:
        valid: bool = True

        if not secrets_path.exists():
            valid = False
            logger.warning(f'The given path for the "--secrets-dir" option does not exist: {secrets_path}')
        elif not secrets_path.is_dir():
            valid = False
            logger.warning(f'The given path for the "--secrets-dir" option is not a directory: {secrets_path}')

        if valid:
            params['secrets_dir'] = secrets_path
            # Ensure the default value gets pushed back into the environment
            os.putenv(f'{env_prefix}_ENV_SECRETS_DIR', str(secrets_path))

    return AppSettings(**params)


base_config: dict = ConfigLoader.load_yaml(DEFAULT_CONFIG_PATH)

settings: AppSettings = load_settings(env_prefix=base_config['app']['environment']['prefix'])

config = Reflective(settings.config)
