from abc import ABC, abstractmethod
from dataclasses import make_dataclass
from typing import Any, List

from common_settings.settings import ApiFields
from database.core import crud
from database.utils.CRUD import CRFactory
from database.utils.decorators import CRUDParameters
from database.common.models import db, PlayersHistory, TeamsHistory
from site_API.common.site_api_settings import headers, params, site, url


db_handle = crud
db_request = CRUDParameters
get_response = site_api.get_response
api_fields = ApiFields()


# @db_request("store", db, PlayersHistory, PlayersRequest)
# class DBStore(CRFactory):
#     pass

# @db_request("store", db, TeamsHistory, TeamsRequest)
# class DBUpdate(CRFactory):
#     pass

# class RequestsInterface():
#
#     @staticmethod
#     def players_request():
#         db_handle.handle("store", db, PlayersHistory, PlayersRequest)
#         retrieved = db_handle.handle("retrieve", db, PlayersHistory, PlayersHistory.id,
#                                      PlayersHistory.first_name, PlayersHistory.last_name)
#
#         data = [f"{retrieve.id} {retrieve.first_name} {retrieve.last_name}" for retrieve in retrieved]
#
#         return data
#
#     @staticmethod
#     def teams_request():
#         db_handle.handle("store", db, TeamsHistory, TeamsRequest)
#         retrieved = db_handle.handle("retrieve", db, TeamsHistory, TeamsHistory.id,
#                                      TeamsHistory.conference, TeamsHistory.full_name)
#
#         data = [f"{retrieve.id} {retrieve.conference} {retrieve.full_name}" for retrieve in retrieved]
#
#         return data


if __name__ == "__main__":

    # RequestsInterface()
    # RequestsInterface.players_request()
    # RequestsInterface.teams_request()
