from click import echo

from src.infrastructure.services import AuthV1ApiService


class LoginInteractor:
    def __init__(self) -> None:
        self.api_service = AuthV1ApiService()

    
    def __call__(self, login: str, password: str):

        response = self.api_service.login(
            login=login,
            password=password
        )

        if response.status_code not in [200, 201]:
            echo(
                f"something gone wrong\n\nDetail:{response.text}"
            )
            return
        
        echo("successful")
