from peewee import (SqliteDatabase,
                    Model,
                    CharField,
                    DateField,
                    BooleanField,
                    ForeignKeyField)


db = SqliteDatabase('bot.sqlite3')


class User(Model):
    chat_id = CharField()

    class Meta:
        database = db


class Planner(Model):
    user = ForeignKeyField(User, on_delete=False)
    task = CharField()
    is_done = BooleanField(default=False)
    date = DateField()

    class Meta:
        database = db


if __name__ == "__main__":
    db.create_tables([User, Planner])
