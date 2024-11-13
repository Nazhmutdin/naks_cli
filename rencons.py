from src.main.app import cli
from src.presentation.commands.auth import auth_group
from src.presentation.commands.parse_naks import parse_group


cli.add_command(auth_group)
cli.add_command(parse_group)


if __name__ == "__main__":
    cli()
