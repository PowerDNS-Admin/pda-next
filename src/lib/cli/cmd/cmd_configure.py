import click
from lib.cli.app import Environment, pass_environment


@click.command('configure', short_help='Builds an environment configuration file based on user input.')
@click.option('-d', '--dry-run', is_flag=True, help='Performs a dry-run of the command without writing any files.')
@pass_environment
def cli(ctx: Environment, dry_run: bool = False):
    """ Builds an environment configuration file based on user input. """

    click.clear()
    click.echo('')
    click.echo('Welcome to the PDA environment configuration wizard!')
    click.echo('')
    click.echo('This wizard will guide you through the process of creating a configuration file for your environment.')
    click.echo('')
    click.echo('What configuration category would you like to work on?')
    click.echo('')
    click.echo('  [1] Environment Type')
    click.echo('  [2] Database')
    click.echo('  [3] Security')
    click.echo('  [4] Email')
    click.echo('  [5] Authentication')
    click.echo('  [7] Other')
    click.echo('  [6] Exit')
    click.echo('')
    click.echo('Enter the number of the category you would like to work on, or press [Enter] to exit.')
    click.echo('')
    click.echo('Your choice: ', nl=False)
    click.echo('')
    click.echo('')

    c = click.getchar()

    click.echo(f'Choice: {c}')
