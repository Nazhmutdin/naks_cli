from requests import Response, Session

from src.config import ApplicationConfig
from src.infrastructure.token_manager import TokenManager


__all__ = [
    "AuthV1ApiService"
]


class AuthV1ApiService(Session):

    def __init__(self) -> None:
        self.token_manager = TokenManager()
        self.base_url = f"{ApplicationConfig.BASE_URL()}/auth/v1"

        super().__init__()


    def login(self, login: str, password: str) -> Response: 
        response = self.post(
            url=f"{self.base_url}/login",
            json={
                "login": login,
                "password": password
            },
            verify=False
        )

        self.token_manager.set_response_tokens(response)

        return response


    def authenticate(self) -> Response:
        response = self.post(
            url = f"{self.base_url}/authenticate",
            cookies={
                "refresh_token": self.token_manager.refresh_token.token
            }
        )

        self.token_manager.set_response_tokens(response)

        return response


    def update_tokens(self) -> Response: 
        response = self.post(
            url = f"{self.base_url}/update-tokens",
            cookies={
                "refresh_token": self.token_manager.refresh_token.token
            }
        )

        self.token_manager.set_response_tokens(response)

        return response


# class ApiV1Service[T](Session):
#     def __init__(self, base_url: str) -> None:
#         self.token_manager = TokenManager()
#         self.auth_api_service = AuthV1ApiService()
#         self._base_url: str = base_url

#         super().__init__()


#     def add(self, data: T) -> Response:
        
#         request = Request(
#             "POST",
#             url=f"{self._base_url}",
#             json=data,
#             cookies={"access_token": self.token_manager.access_token.token}
#         )

#         return self._execute(request)


#     def get_one(self, ident: str) -> Response:
        
#         request = Request(
#             "GET",
#             url=f"{self._base_url}/{ident}",
#             cookies={"access_token": self.token_manager.access_token.token}
#         )

#         return self._execute(request)


#     def update(self, ident: str, data: T) -> Response:
        
#         request = Request(
#             "PATCH",
#             url=f"{self._base_url}/{ident}",
#             json=data,
#             cookies={"access_token": self.token_manager.access_token.token}
#         )

#         return self._execute(request)


#     def remove(self, ident: str) -> Response:
#         request = Request(
#             "DELETE",
#             url=f"{self._base_url}/{ident}",
#             cookies={"access_token": self.token_manager.access_token.token}
#         )

#         return self._execute(request)
    

#     def _execute(self, request: Request) -> Response:

#         response = self._send(request)

#         if response.status_code == 200:
#             return response
        
#         elif response.status_code != 200 and "access token expired" in response.text:
#             response = self.auth_api_service.authenticate()

#             if response.status_code == 200:
#                 request.cookies["access_token"] = self.token_manager.access_token.token
#                 response = self._send(request)

#             elif response.status_code != 200 and "refresh token expired" in response.text:
#                 response = self.auth_api_service.update_tokens()

#                 if response.status_code == 200:
#                     request.cookies["access_token"] = self.token_manager.access_token.token
#                     response = self._send(request)
                
#                 return response
            
#             else:
#                 return response
        
#         else:
#             return response

    
#     def _send(self, request: Request) -> Response:
#         return self.send(self.prepare_request(request))
            

# @overload
# def api_service_maker(mode: WelderMode) -> ApiV1Service[WelderData]: ...

# @overload
# def api_service_maker(mode: NDTMode) -> ApiV1Service[NDTData]: ...

# @overload
# def api_service_maker(mode: WelderCertificationMode) -> ApiV1Service[WelderCertificationData]: ...

# def api_service_maker(mode: Literal["welder", "welder_certification", "ndt"]):
#     match mode:
#         case "ndt":
#             return ApiV1Service(f"{Settings.BASE_URL()}/v1/ndts")
#         case "welder":
#             return ApiV1Service(f"{Settings.BASE_URL()}/v1/welders")
#         case "welder_certification":
#             return ApiV1Service(f"{Settings.BASE_URL()}/v1/welder-certifications")
#         case _:
#             raise ValueError("invalid mode")
        