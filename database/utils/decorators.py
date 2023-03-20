from typing import Any, Callable, TypeVar

from database.utils.CRUD import CRFactory
# from database.core import crud
from database.common.models import db


T = TypeVar('T')

class CRUDParameters():

    def __init__(self, command: str, db: db, model: T, *args) -> None:
        self.command = command
        self.db = db
        self.model = model
        self.args = *args,

    def __call__(self, object: CRFactory) -> Callable:
        return object.handle(self.command, self.db, self.model, *self.args)


if __name__ == "__main__":

    CRUDParameters
