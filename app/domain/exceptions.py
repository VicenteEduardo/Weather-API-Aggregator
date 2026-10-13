# erros nossos, para depois a API traduzir para 404/502 etc
class DomainError(Exception):
    pass


class CityNotFound(DomainError):
    pass


class InvalidQuery(DomainError):
    pass


class ProviderUnavailable(DomainError):
    pass
