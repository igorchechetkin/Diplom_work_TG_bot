from database.utils.CRUD import CRFactory
from database.common.models import db, PlayersHistory, TeamsHistory


db.connect()
db.create_tables([PlayersHistory])
db.create_tables([TeamsHistory])


crud = CRFactory

if __name__== "__main__":

    crud()
