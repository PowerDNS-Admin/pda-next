from pathlib import Path
from reflective import Reflective
from app.model.settings import AppSettings
from app.util.config import ConfigBuilder


class Environment:
    """ The application environment class that provides access to the environment settings and configuration. """

    _settings: AppSettings = None
    """ The environment settings. """

    _config: Reflective = None
    """ The environment configuration. """

    @property
    def settings(self) -> AppSettings:
        """ Returns the app's settings. """
        return self._settings

    @settings.setter
    def settings(self, value: AppSettings):
        """ Sets the app's settings. """
        self._settings = value
        if self.config is None:
            self._config = Reflective(value.config)

    @property
    def config(self) -> Reflective:
        """ Returns the environment configuration. """
        return self._config

    @property
    def c(self) -> Reflective:
        """ Returns the environment configuration. """
        return self._config

    @property
    def debug(self) -> bool:
        """ Returns whether debug mode is enabled. """
        return self._settings.debug if isinstance(self._settings, AppSettings) else False

    def save(self, path: str or Path = None) -> None:
        """ Saves the current configuration to the given path, or the default if None given. """
        if path is None:
            path = self.settings.config_path
        ConfigBuilder.save_yaml(path, self._config.ref)
