from click import Command, Option, group
from dishka import FromDishka

from src.application.interactors.auth import LoginInteractor


class LoginCommand(Command): 
    def __init__(self):
        name = "login"

        params= [
            Option(["--login", "-l"], type=str, prompt=True, required=True),
            Option(["--password", "-p"], type=str, prompt=True, required=True, hide_input=True)
        ]

        super().__init__(
            name=name,
            params=params,
            callback=self.execute
        )

    
    def execute(self, login: str, password: str, login_action: FromDishka[LoginInteractor]):
        login_action(
            login=login,
            password=password
        )


@group("auth")
def auth_group(): ...


auth_group.add_command(LoginCommand())
