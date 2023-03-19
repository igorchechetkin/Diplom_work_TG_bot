from abc import ABC, abstractmethod
import logging

from logger.core import logged
import requests


class _AbstractResponse(ABC):

    @abstractmethod
    def make_response(self):
        pass

    @abstractmethod
    def get_info(self):
        pass


class Response(_AbstractResponse):

    SUCCESS: int = 200

    headers: dict = None
    log_info: str = None
    method: str = None
    params: dict = None
    timeout: int = None
    url: str = None

    @logged
    def make_response(self) -> requests.Response:
        response = requests.request(
            self.method,
            self.url,
            headers=self.headers,
            params=self.params,
            timeout=self.timeout
        )

        return response

    def get_info(self) -> requests.Response:

        logging.info(self.log_info)

        response = self.make_response()

        if response.status_code == self.SUCCESS:

            return response

        return response.status_code


class _PlayersGet(Response):
    pass


class _TeamsGet(Response):
    pass


class SiteApiFactory():

    GET_SITE_API = {
        "get_players": _PlayersGet,
        "get_teams": _TeamsGet
    }

    @classmethod
    def get_response(cls, command: str, **request_parameters) -> requests.Response:

        response = cls.GET_SITE_API.get(command)

        if response:
            response = response()

            for key, value in request_parameters.items():
                setattr(response, key, value)

            return response.get_info()


if __name__ == "__main__":

    SiteApiFactory()
