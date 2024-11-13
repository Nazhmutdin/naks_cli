from dishka import Provider, Scope, provide

from src.application.interactors import LoginInteractor, ParsePersonalNaksCertificationsInteractor


class DependecyProvider(Provider):

    @provide(scope=Scope.APP)
    def provide_login_interactor(self) -> LoginInteractor:
        return LoginInteractor()


    @provide(scope=Scope.APP)
    def provide_parse_personal_naks_certifications_interactor(self) -> ParsePersonalNaksCertificationsInteractor:
        return ParsePersonalNaksCertificationsInteractor()
