from app.cli.entry import cli


@cli.group('config')
def group():
    """Manages the app configuration."""
    pass
