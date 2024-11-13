from requests_mock import Mocker

from infrastructure.services.api import AuthV1ApiService
from funcs import create_access_token_cookie, create_refresh_token_cookie


class TestAuthApiService:
    service = AuthV1ApiService()

    def test_login(self) -> None:
        access_token = self.service.token_manager.access_token
        refresh_token = self.service.token_manager.refresh_token
        mock = Mocker()

        

        access_token_header = tuple(create_access_token_cookie().output().split(": "))
        refresh_token_header = tuple(create_refresh_token_cookie().output().split(": "))

        with mock:
            mock.post(
                url=f"{self.service.base_url}/login",
                headers=[access_token_header, refresh_token_header],
                status_code=200
            )

            res = self.service.login(
                "TestLogin",
                "TestPassword"
            )

            assert res.status_code == 200
            assert mock.last_request.path == "/auth/v1/login"
            assert mock.last_request.text == '{"login": "TestLogin", "password": "TestPassword"}'
            assert access_token != self.service.token_manager.access_token
            assert refresh_token != self.service.token_manager.refresh_token


    def test_authenticate(self) -> None:
        access_token = self.service.token_manager.access_token
        mock = Mocker()
        

        access_token_header = tuple(create_access_token_cookie().output().split(": "))

        with mock:
            mock.post(
                url=f"{self.service.base_url}/authenticate", 
                status_code=200,
                headers=[access_token_header],
            )

            res = self.service.authenticate()

            assert res.status_code == 200
            assert mock.last_request.path == "/auth/v1/authenticate"
            assert access_token != self.service.token_manager.access_token

    
    def test_update_tokens(self) -> None:
        access_token = self.service.token_manager.access_token
        refresh_token = self.service.token_manager.refresh_token
        mock = Mocker()
        

        access_token_header = tuple(create_access_token_cookie().output().split(": "))
        refresh_token_header = tuple(create_refresh_token_cookie().output().split(": "))


        with mock:
            mock.post(
                url=f"{self.service.base_url}/update-tokens", 
                headers=[access_token_header, refresh_token_header],
                status_code=200
            )

            res = self.service.update_tokens()


            assert res.status_code == 200
            assert mock.last_request.path == "/auth/v1/update-tokens"
            assert access_token != self.service.token_manager.access_token
            assert refresh_token != self.service.token_manager.refresh_token


# class BaseTestApiV1Service[T]:
#     service: ApiV1Service[T]
#     data_path_ident: str


#     def test_add(self, data: T) -> None:
#         mock = Mocker()

#         with mock:
#             mock.post(
#                 url=self.service._base_url, 
#                 status_code=200
#             )

#             res = self.service.add(data)


#             assert res.status_code == 200
#             assert mock.last_request.path == f"/v1/{self.data_path_ident}"


#     def test_get(self, ident: str) -> None:
#         mock = Mocker()

#         with mock:
#             mock.get(
#                 url=f"{self.service._base_url}/{ident}", 
#                 status_code=200
#             )

#             res = self.service.get_one(ident)


#             assert res.status_code == 200
#             assert mock.last_request.path == f"/v1/{self.data_path_ident}/{ident.lower()}"


#     def test_update(self, ident: str, data: T) -> None:
#         mock = Mocker()

#         with mock:
#             mock.patch(
#                 url=f"{self.service._base_url}/{ident}", 
#                 status_code=200
#             )

#             res = self.service.update(ident, data)


#             assert res.status_code == 200
#             assert mock.last_request.path == f"/v1/{self.data_path_ident}/{ident.lower()}"


#     def test_delete(self, ident: str) -> None:
#         mock = Mocker()

#         with mock:
#             mock.delete(
#                 url=f"{self.service._base_url}/{ident}", 
#                 status_code=200
#             )

#             res = self.service.remove(ident)


#             assert res.status_code == 200
#             assert mock.last_request.path == f"/v1/{self.data_path_ident}/{ident.lower()}"


# class TestWelderDBService(BaseTestApiV1Service[WelderData]):
#     service = api_service_maker("welder")
#     data_path_ident = "welders"


#     @pytest.mark.usefixtures('welders')
#     def test_add(self, welders: list[WelderData]) -> None:
#         super().test_add(welders[0])


#     @pytest.mark.usefixtures('welders')
#     @pytest.mark.parametrize(
#             "attr, index",
#             [
#                 ("kleymo", 1), 
#                 ("ident", 7), 
#                 ("kleymo", 31), 
#                 ("ident", 80)
#             ]
#     )
#     def test_get(self, attr: str, index: int, welders: list[WelderData]) -> None:
#         welder = welders[index]

#         ident = welder[attr]

#         super().test_get(ident)

    
#     @pytest.mark.parametrize(
#         "ident, data",
#         [
#             ("095898d1419641b3adf45af287aad3e7", {"name": "dsdsds", "birthday": "15.12.1995"}),
#             ("dc20817ed3844660a69b5c89d7df15ac", {"passport_number": "T15563212", "sicil": "1585254"}),
#             ("d00b26c65fdf4a819c5065e301dd81dd", {"nation": "RUS", "status": 1}),
#         ]
#     )
#     def test_update(self, ident: str, data: dict) -> None:

#         super().test_update(ident, data)


#     @pytest.mark.usefixtures('welders')
#     @pytest.mark.parametrize(
#             "index",
#             [0, 34, 65, 1, 88, 90]
#     )
#     def test_delete(self, welders: list[WelderData], index: int) -> None:
#         super().test_delete(welders[index]["kleymo"])


# class TestWelderCertificationDBService(BaseTestApiV1Service[WelderCertificationData]):
#     service = api_service_maker("welder_certification")
#     data_path_ident = "welder-certifications"


#     @pytest.mark.usefixtures('welder_certifications')
#     def test_add(self, welder_certifications: list[WelderCertificationData]) -> None:
#         super().test_add(welder_certifications[0])


#     @pytest.mark.usefixtures('welder_certifications')
#     @pytest.mark.parametrize(
#             "index",
#             [1, 7, 31, 80]
#     )
#     def test_get(self, index: int, welder_certifications: list[WelderCertificationData]) -> None:
#         cert = welder_certifications[index]

#         ident = cert["ident"]

#         super().test_get(ident)


#     @pytest.mark.parametrize(
#             "ident, data",
#             [
#                 ("cccba2a0ea9047c8837691a740513f6d", {"welding_materials_groups": ["dsdsds"], "certification_date": "15.12.1995"}),
#                 ("422786ffabd54d74867a8f34950ee0b5", {"job_title": "ппмфва", "kleymo": "11F9", "expiration_date": "1990-05-15"}),
#                 ("71c20a79706d4fb28f7b84e94881565c", {"insert": "В1", "company": "asasas", "expiration_date_fact": "2025-10-20"}),
#                 ("435a9de3ade64c38b316dd08c3c7bc7c", {"connection_type": "gggg", "outer_diameter_from": 11.65, "details_type": ["2025-10-20", "ffff"]}),
#             ]
#     )
#     def test_update(self, ident: str, data: dict) -> None:
#         super().test_update(ident, data)


#     @pytest.mark.usefixtures('welder_certifications')
#     @pytest.mark.parametrize(
#             "index",
#             [0, 34, 65, 1, 88, 90]
#     )
#     def test_delete(self, welder_certifications: list[WelderCertificationData], index: int) -> None:
#         super().test_delete(welder_certifications[index]["ident"])



# class TestNDTDBService(BaseTestApiV1Service[NDTData]):
#     service = api_service_maker("ndt")
#     data_path_ident = "ndts"


#     @pytest.mark.usefixtures('ndts')
#     def test_add(self, ndts: list[NDTData]) -> None:
#         super().test_add(ndts)


#     @pytest.mark.usefixtures('ndts')
#     @pytest.mark.parametrize(
#             "index",
#             [1, 7, 31, 80]
#     )
#     def test_get(self, index: int, ndts: list[NDTData]) -> None:
#         ident = ndts[index]["ident"]
        
#         super().test_get(ident)


#     @pytest.mark.parametrize(
#             "ident, data",
#             [
#                 ("97c1a8b30a764bae84be20dab742644a", {"kleymo": "11F9", "company": "adsdsad"}),
#                 ("0d92a1ae45f942a5bfba4d26b8a34cd7", {"subcompany": "ппмffфва", "welding_date": "1990-05-15"}),
#                 ("45c040e0a78e4a3994b6cc12d3ba3d81", {"total_weld_1": 0.5, "total_weld_2": 5.36}),
#             ]
#     )
#     def test_update(self, ident: str, data: dict) -> None:
#         super().test_update(ident, data)


#     @pytest.mark.usefixtures('ndts')
#     @pytest.mark.parametrize(
#             "index",
#             [0, 34, 65, 1, 88, 90]
#     )
#     def test_delete(self, ndts: list[NDTData], index: int) -> None:
#         super().test_delete(ndts[index]["ident"])
