from database.common.models import db, PlayersHistory, TeamsHistory
from database.utils.CRUD import CRFactory
from database.utils.decorators import CRUDParameters
from site_API.core import RequestsFactory


db.connect()
db.create_tables([PlayersHistory])
db.create_tables([TeamsHistory])


site_api = RequestsFactory
db_request = CRUDParameters
crud = CRFactory


@db_request("store", db, PlayersHistory, site_api.site_api_handle("players"))
class DBStorePlayers(CRFactory):
    pass


@db_request("store", db, TeamsHistory, site_api.site_api_handle("teams"))
class DBStoreTeams(CRFactory):
    pass


@db_request("retrieve", db, PlayersHistory, PlayersHistory.id, PlayersHistory.first_name, PlayersHistory.last_name)
class DBRetrievePlayers(CRFactory):
    pass


@db_request("retrieve", db, TeamsHistory, TeamsHistory.id, TeamsHistory.conference, TeamsHistory.full_name)
class DBRetrieveTeams(CRFactory):
    pass


class DBFactory():

    STORED = {
        "db_players": DBStorePlayers,
        "db_teams": DBStoreTeams
    }

    RETRIEVED = {
        "db_players": DBRetrievePlayers,
        "db_teams": DBRetrieveTeams
    }

    @classmethod
    def handle(cls, command: str):

        cls.STORED.get(command)

        data = cls.RETRIEVED.get(command)

        if data:
            return data


if __name__ == "__main__":

    DBFactory()
