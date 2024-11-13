from http.cookies import SimpleCookie, Morsel
from datetime import datetime
from enum import Enum

from requests import Response

from src.infrastructure.dto import AccessTokenShema, RefreshTokenShema, TokensDataShema
from src.utils.funcs import read_json, save_json
from src.config import ApplicationConfig


class TokenTypeEnum(Enum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"


class TokenManager: 

    @property
    def access_token(self) -> AccessTokenShema:
        data = self._read_tokens_json()

        return data.access_token
    

    @access_token.setter
    def access_token(self, value: AccessTokenShema) -> None:
        data = self._read_tokens_json()

        data.access_token = value

        self._save_tokens_json(data)


    @property
    def refresh_token(self) -> RefreshTokenShema:
        data = self._read_tokens_json()

        return data.refresh_token
    

    @refresh_token.setter
    def refresh_token(self, value: RefreshTokenShema) -> None:
        data = self._read_tokens_json()

        data.refresh_token = value

        self._save_tokens_json(data)


    def set_response_tokens(self, response: Response):

        cookies = SimpleCookie()

        cookies.load(response.headers["Set-Cookie"])


        for key, morsel in cookies.items():
            self._set_token(
                key=key,
                morsel=morsel
            )


    def _set_token(self, key: str, morsel: Morsel):
        if key in TokenTypeEnum:
            setattr(
                self,
                key,
                self._to_token_shema(morsel, key)
            )
            
    
    def _to_token_shema(self, morsel: Morsel, key: str):
        token= morsel.value
        exp_dt=datetime.strptime(morsel["expires"], "%a, %d %b %Y %H:%M:%S GMT")

        key = TokenTypeEnum[key.upper()]

        match key:
            case TokenTypeEnum.ACCESS_TOKEN:
                return AccessTokenShema(token=token, exp_dt=exp_dt)
            case TokenTypeEnum.REFRESH_TOKEN:
                return RefreshTokenShema(token=token, exp_dt=exp_dt)
        

    def _read_tokens_json(self) -> TokensDataShema:

        return TokensDataShema.model_validate(read_json(ApplicationConfig.TOKENS_JSON_PATH()))
            

    def _save_tokens_json(self, data: TokensDataShema) -> None:

        return save_json(data.model_dump(mode="json"), ApplicationConfig.TOKENS_JSON_PATH())
