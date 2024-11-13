from click import Context, group, pass_context
from dishka import make_container
from dishka.integrations.click import setup_dishka

from src.main.dependencies import DependecyProvider


@group()
@pass_context
def cli(context: Context) -> None:
    container = make_container(DependecyProvider())
    setup_dishka(container=container, context=context, auto_inject=True)
