import click
from cryptography.fernet import Fernet
from lib.cli.app import Environment, pass_environment


@click.command('gen-salt', short_help='Generates a Fernet encryption key to be used for data encryption.')
@click.option('-r', '--raw', is_flag=True, help='Prints the raw value without a label. (Default: False)')
@pass_environment
def cli(ctx: Environment, raw: bool = False):
    """ Generates a Fernet encryption key to be used for data encryption. """
    key: str = Fernet.generate_key().decode("utf-8")
    if raw:
        print(key)
    else:
        print(f'Generated Key: {Fernet.generate_key().decode("utf-8")}')
