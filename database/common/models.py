from datetime import datetime

import peewee as pw


db = pw.SqliteDatabase("users_requests_history.db")


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())

    class Meta():
        database = db


class PlayersHistory(ModelBase):
    id = pw.TextField()
    first_name = pw.TextField()
    last_name = pw.TextField()


class TeamsHistory(ModelBase):
    id = pw.TextField()
    conference = pw.TextField()
    full_name = pw.TextField()


#TODO Можно ли класс хистори создать из одной точки (датакласс).
#TODO дока пиви (динамическое создание полей)