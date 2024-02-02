import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Union
from app.util.config import ConfigLoader

DEFAULT_CONFIG_PATH: Path = Path('defaults.yml')
base_config: dict = ConfigLoader.load_yaml(DEFAULT_CONFIG_PATH)


class AppSettings(BaseSettings):
    """ The application settings class that loads setting values from the application environment. """

    _config: Union[dict, None] = None
    """ Additional configuration settings loaded automatically from the YAML file given in the config_path setting. """

    config_path: Union[str, Path] = 'config.yml'
    """ The path to the YAML file containing additional configuration settings. """

    debug: bool = False
    """ Whether debug mode is enabled. """

    env_file: Union[str, Path, None] = None
    """ The path to the environment file to load settings from. """

    env_file_encoding: str = 'UTF-8'
    """ The file encoding of the environment file to load settings from. """

    env_secrets_dir: Union[str, Path, None] = None
    """ The path to the secrets directory to load environment variable values from. """

    root_path: Union[str, Path] = Path(os.getcwd())
    """ The root path of the application which is typically the project repository root directory. """

    version: str = base_config['app']['version']
    """ The application version number """

    @property
    def config(self) -> dict:
        """ Returns the configuration data provided by the YAML file given in the config_path setting. """

        # Load the YAML configuration file if it exists and has not already been loaded
        if self._config is None:
            if DEFAULT_CONFIG_PATH.exists():
                self._config = ConfigLoader.load_yaml(DEFAULT_CONFIG_PATH)

            if isinstance(self.config_path, Path | str) and Path(self.config_path).exists():
                user_config = ConfigLoader.load_yaml(self.config_path)

                if user_config is None:
                    return self._config

                if self._config is None:
                    self._config = user_config
                else:
                    self._config.update(user_config)

        return self._config

    class Config:
        env_prefix = base_config['app']['environment']['prefix'] + '_'
        env_nested_delimiter = '__'
