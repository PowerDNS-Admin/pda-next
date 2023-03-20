import click
import os
import subprocess
from lib.cli.app import Environment, pass_environment


@click.command("run", short_help="Run the application with the appropriate server based on the environment.")
@pass_environment
def cli(ctx: Environment):
    """ Run the application with the appropriate server based on the environment."""

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pda.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    command: list

    # Run the application with Gunicorn HTTP/WSGI server for production environment types
    if ctx.settings.env_type == 'production':
        server_args: list = ['--workers=3', '--threads=3', '--timeout=0', '--log-level=info',
                             '--log-file=-', '--access-logfile=-', '--error-logfile=-', '--enable-stdio-inheritance',
                             '--capture-output', f'--bind={ctx.settings.server_address}:{ctx.settings.server_port}']
        server_env = os.environ.copy()
        server_env['GUNICORN_CMD_ARGS'] = ' '.join(server_args)
        subprocess.run(['gunicorn', 'src.pda.wsgi'], env=server_env)

    # Run the application with Django built-in HTTP server for all unmatched environment types
    else:
        execute_from_command_line(
            ['src/manage.py', 'runserver', f'{ctx.settings.server_address}:{ctx.settings.server_port}']
        )
