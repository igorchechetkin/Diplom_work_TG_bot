from typing import Callable, Dict, List, TypeVar

from peewee import ModelSelect

from database.common.models import ModelBase
from ..common.models import db


T = TypeVar('T')


class _Store():

    def store_data(db: db, model: T, *data: List[Dict]) -> None:

        with db.atomic():
            model.insert_many(*data).execute()


class _Retrieve():

    def retrieve_data(db: db, model: T, *columns: ModelBase) -> ModelSelect:

        with db.atomic():
            response = model.select(*columns)

        return response


class CRFactory():

    CRUD = {
        "store": _Store.store_data,
        "retrieve": _Retrieve.retrieve_data
    }

    @classmethod
    def handle(cls, command: str, db: db, model: T, *args) -> Callable:

        method = cls.CRUD.get(command)

        if method:
            return method(db, model, *args)


if __name__ == "__main__":

    CRFactory()
