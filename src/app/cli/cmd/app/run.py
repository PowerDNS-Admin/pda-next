from app.cli import Environment
from app.cli.entry import pass_environment
from . import group


@group.command('run')
@pass_environment
def wrapper(env: Environment):
    """Runs the application with the configured server type."""
    return command(env)


def command(env: Environment) -> bool:
    """Runs the application with the configured server type."""
    import os
    import subprocess
    
    c = env.config
    task: list = []

    if c.server.type not in ['django', 'gunicorn', 'uvicorn', 'uwsgi']:
        print(f'Invalid server type: {c.server.type}')
        exit(1)

    server_env = os.environ.copy()

    # Run the application with Gunicorn HTTP/WSGI server
    if c.server.type == 'gunicorn':
        command_args: list = [f'--workers={c.server.workers}', f'--threads={c.server.threads}',
                              f'--timeout={c.server.gunicorn.timeout}',
                              f'--log-level={c.server.gunicorn.log_level}',
                              '--log-file=-', '--access-logfile=-', '--error-logfile=-', '--enable-stdio-inheritance',
                              '--capture-output', f'--bind={c.server.address}:{c.server.port}']

        if c.server.auto_reload:
            command_args += ['--reload-engine', 'auto']

        server_env['GUNICORN_CMD_ARGS'] = ' '.join(command_args)

        task += ['gunicorn', 'pda.wsgi:application']

        subprocess.run(task, env=server_env, stdout=subprocess.PIPE)

    # Run the application with Uvicorn ASGI server
    elif c.server.type == 'uvicorn':
        task += ['uvicorn', '--host', c.server.address, '--port', str(c.server.port),
                 '--root-path', c.server.proxy_root,
                 '--log-level', f'{c.server.uvicorn.log_level}', '--access-log',
                 '--workers', f'{c.server.workers}',
                 '--proxy-headers']

        if c.server.auto_reload:
            task += ['--reload']

        task += ['pda.asgi:application']

        subprocess.run(task, env=server_env, stdout=subprocess.PIPE)

    # Run the application with UWSGI server
    elif c.server.type == 'uwsgi':
        task += ['uwsgi', '--http-socket', f'{c.server.address}:{c.server.port}',
                 '--workers', f'{c.server.workers}', '--threads', f'{c.server.threads}',
                 '--master', '--enable-threads', '--plugins', 'python3',
                 '--wsgi-file']

        task += ['src/pda/wsgi.py']

        subprocess.run(task, env=server_env, stdout=subprocess.PIPE)

    # Run the application with Gunicorn HTTP/WSGI server
    elif c.server.type == 'django':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pda.settings')

        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc

        execute_from_command_line(
            ['src/manage.py', 'runserver', f'{c.server.address}:{c.server.port}']
        )

    return True
