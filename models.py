from peewee import SqliteDatabase, Model, CharField, TimeField

# Set DataBase
db = SqliteDatabase('report.db')

class Racer(Model):
    abbr_name = CharField()
    name = CharField(unique=True)
    team = CharField()
    result = TimeField()

    class Meta:
        database = db
        db_table = 'racers'


if __name__ == '__main__':
    db.create_tables([Racer])