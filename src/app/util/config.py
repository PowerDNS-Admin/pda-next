import os
import re
import typing
import yaml
from pathlib import Path
from typing import Union


class ConfigBuilder:
    """A class for building configuration files."""

    @staticmethod
    def save_yaml(path: Union[str, Path], config: dict) -> None:
        """Saves the given configuration dictionary to the given YAML file path."""

        with open(str(path), 'w') as f:
            yaml.dump(config, f)
            f.close()

    @staticmethod
    def build_env_file(config: dict) -> str:
        """Builds a .env style file from the given configuration dictionary."""
        env_file: str = ''
        config = ConfigParser.parse(config, config)
        env_config = ConfigUtil.flatten(config)

        for key, value in env_config.items():
            if isinstance(value, bool):
                value = str(value).lower()
            elif isinstance(value, list):
                value = ','.join(value)
            elif isinstance(value, dict):
                value = ','.join([f'{k}:{v}' for k, v in value.items()])
            elif isinstance(value, str):
                value = value.strip()
                if ' ' in value:
                    value = f'"{value}"'

            env_file += f'{key}={value}\n'

        return env_file

    @staticmethod
    def build_tpl(template: Union[str, Path], config: dict, parse: bool = True) -> str:
        """Builds a configuration file from the given template and configuration dictionary."""
        from jinja2 import Environment, FileSystemLoader

        if not isinstance(template, Path):
            template = Path(template)

        if not template.exists():
            raise FileNotFoundError(f'Failed to find the template file: {template}')

        env = Environment(loader=FileSystemLoader(str(template.parent)), autoescape=True)
        tpl = env.get_template(template.name)
        tpl_content = tpl.render(config)

        if parse:
            tpl_content = ConfigParser.parse_string(config, tpl_content)

        return tpl_content


class ConfigLoader:
    """A class for loading simple configuration settings from a text file."""

    @staticmethod
    def load_file(path: Path or str) -> dict:
        """Loads the given configuration file and returns a dictionary of key/value pairs."""
        config: dict = {}

        if not os.path.exists(path):
            return config

        with open(path) as f:
            for line in f.read().splitlines():
                key, value = line.split('=')
                config[key.strip().lower()] = value.strip()
            f.close()

        return config

    @staticmethod
    def load_yaml(path: Path or str) -> dict:
        """Loads the given configuration file and returns a dictionary of key/value pairs."""
        from yaml import YAMLError

        config: dict = {}

        if not isinstance(path, Path):
            path = Path(path)

        if not path.exists():
            return config

        try:
            with open(path, 'r') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                f.close()
        except FileNotFoundError:
            # print(f'The given path for the configuration file does not exist: {config_path}')
            pass
        except IsADirectoryError:
            # print(f'The given path for the configuration file is not a file: {config_path}')
            pass
        except PermissionError:
            # print(f'Permission denied when trying to read the configuration file: {config_path}')
            pass
        except UnicodeDecodeError:
            # print(f'Failed to decode the configuration file: {config_path}')
            pass
        except YAMLError as e:
            # print(f'Failed to parse the configuration file "{config_path}": {e}')
            pass

        return config


class ConfigParser:
    """A class for parsing variable references from values."""

    ref_pattern = re.compile(r'\$(c|e){([a-z_]+[a-z0-9_/]*)}', re.IGNORECASE)
    """ The regular expression pattern used to match variable references in values. """

    @staticmethod
    def reference(config: dict, key: str, default: any = None, parse: bool = True) -> any:
        """ Returns the configuration value for the given key, or the given default if not found. """
        from functools import reduce

        segment_boundary = '/' if '/' in key else '__'
        segments = key.split(segment_boundary)

        try:
            result = reduce(lambda c, k: c[k] if not k.isnumeric() else c[int(k)], segments, config)
        except (KeyError, TypeError):
            result = default
        if parse:
            result = ConfigParser.parse(config, result)
        return result

    @staticmethod
    def update(config: dict, key: str, value: any) -> dict:
        """ Updates the configuration value for the given key. """

        ref = config
        segment_boundary = '/' if '/' in key else '__'
        segments = key.split(segment_boundary)

        for k in segments[:-1]:
            ref = ref[k if not k.isnumeric() else int(k)]

        ref[segments[-1]] = value

        return config

    @staticmethod
    def parse(config: dict, value: any, default: any = None) -> any:
        """ Parses the given value for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        result = value.copy() if (isinstance(value, dict) or isinstance(value, list)) else value

        if isinstance(result, str):
            result = ConfigParser.parse_string(config, result, default)

        elif isinstance(result, list):
            result = ConfigParser.parse_list(config, result, default)

        elif isinstance(result, dict):
            result = ConfigParser.parse_dict(config, result, default)

        return result

    @staticmethod
    def parse_string(config: dict, value: str, default: any = None) -> str:
        """ Parses the given string for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        # Process $(c|e){...} references
        matches = ConfigParser.ref_pattern.findall(value)

        for match in matches:
            ref = str(match[0]).lower()
            if ref == 'c':
                config_value = ConfigParser.reference(config, match[1], default, True)
                value = value.replace(f'${match[0]}{{{match[1]}}}', str(config_value))
            elif ref == 'e':
                env_value = os.getenv(match[1])
                value = value.replace(f'${match[0]}{{{match[1]}}}', str(env_value))

        return value

    @staticmethod
    def parse_list(config: dict, value: list, default: any = None) -> list:
        """ Parses the given list for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        result = []

        for item in value:
            result.append(ConfigParser.parse(config, item, default))

        return result

    @staticmethod
    def parse_dict(config: dict, value: dict, default: any = None) -> dict:
        """ Parses the given dictionary for configuration references, updating the values with current configuration
        values, and returning the updated copy. """

        result = {}

        for k, v in value.items():
            result[k] = ConfigParser.parse(config, v, default)

        return result


class ConfigUtil:
    """A class for working with configuration related data and files."""

    @staticmethod
    def flatten(config: dict, prefix: str = '') -> dict:
        result: dict = {}

        for key, value in config.items():
            key = key.upper()

            # Test the key with a regex to ensure it is a valid environment variable name
            if not re.match(r'^[A-Z_][A-Z0-9_]*$', key):
                continue

            if isinstance(value, dict):
                result.update(ConfigUtil.flatten(value, f'{prefix}{key}__'))
            else:
                result[f'{prefix}{key}'] = value

        return result
