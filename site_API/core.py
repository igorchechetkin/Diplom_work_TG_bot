from abc import ABC, abstractmethod
from dataclasses import make_dataclass
from typing import Any, Dict, List

from common_settings.settings import ApiFields
from site_API.utils.site_api_handler import SiteApiFactory
from site_API.common.site_api_settings import headers, params, site, url


site_api = SiteApiFactory()
get_response = site_api.get_response
api_fields = ApiFields()


_request_parameters: dict = {"method": "GET", "url": None, "headers": headers, "params": params,
                          "timeout": site.api_timeout, "log_info": None}


class RequestAbstract(ABC):

    @abstractmethod
    def make_request(self, *args, **kwargs):
        pass


class RequestAPI(RequestAbstract):

    fields: ApiFields

    @classmethod
    def make_request(cls, command: str, **_request_parameters) -> List:

        response = get_response(command, **_request_parameters)
        response = response.json()
        response = response.get("data")

        absolutely_data = (
            (make_dataclass("Data", [(key, value) for key, value in field.items() if key in cls.fields]))
            for field in response
        )

        data = [player.__annotations__ for player in absolutely_data]

        return data


class UpdateResponseParameters():

    def __init__(self, command: str, _request_parameters: dict, **kwargs) -> None:
        self.command = command
        self.request_parameters = _request_parameters
        self.request_parameters.update(**kwargs)

    def __call__(self, request: RequestAPI) -> Any:
        return request.make_request(self.command, **self.request_parameters)


update_params = UpdateResponseParameters


@update_params("get_players", _request_parameters,
               **{"url": url + "/players", "log_info": "Запрос на сбор информации о всех игроках"})
class PlayersRequest(RequestAPI):
    fields = api_fields.fields_players.split()


@update_params("get_teams", _request_parameters,
               **{"url": url + "/teams", "log_info": "Запрос на сбор информации о всех командах"})
class TeamsRequest(RequestAPI):
    fields = api_fields.fields_teams.split()


class RequestsFactory():

    REQUESTS = {
        "players": PlayersRequest,
        "teams": TeamsRequest
    }

    @classmethod
    def site_api_handle(cls, command: str) -> List[Dict]:

        request = cls.REQUESTS.get(command)

        if request:
            return request


if __name__ == "__main__":

    RequestsFactory()
