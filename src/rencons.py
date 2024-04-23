from click import group
from commands import welder_commands, welder_certification_commands, ndt_commands, naks_commands


@group
def cli() -> None:
    ...

cli.add_command(welder_commands)
cli.add_command(welder_certification_commands)
cli.add_command(ndt_commands)
cli.add_command(naks_commands)


if __name__ == "__main__":
    cli()
