from abc import ABC, abstractmethod
from dataclasses import make_dataclass
from typing import Any, List

from common.settings import ApiFields
from database.core import crud
from database.utils.CRUD import CRFactory
from database.utils.decorators import CRUDParameters
from database.common.models import db, PlayersHistory, TeamsHistory
from site_API.core import headers, params, site, site_api, url


db_handle = crud
db_request = CRUDParameters
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


# @db_request("store", db, PlayersHistory, PlayersRequest)
# class DBStore(CRFactory):
#     pass

# @db_request("store", db, TeamsHistory, TeamsRequest)
# class DBUpdate(CRFactory):
#     pass

class RequestsInterface():

    @staticmethod
    def players_request():
        db_handle.handle("store", db, PlayersHistory, PlayersRequest)
        retrieved = db_handle.handle("retrieve", db, PlayersHistory, PlayersHistory.id,
                                     PlayersHistory.first_name, PlayersHistory.last_name)

        data = [f"{retrieve.id} {retrieve.first_name} {retrieve.last_name}" for retrieve in retrieved]

        return data

    @staticmethod
    def teams_request():
        db_handle.handle("store", db, TeamsHistory, TeamsRequest)
        retrieved = db_handle.handle("retrieve", db, TeamsHistory, TeamsHistory.id,
                                     TeamsHistory.conference, TeamsHistory.full_name)

        data = [f"{retrieve.id} {retrieve.conference} {retrieve.full_name}" for retrieve in retrieved]

        return data


if __name__ == "__main__":

    RequestsInterface()
    RequestsInterface.players_request()
    RequestsInterface.teams_request()
