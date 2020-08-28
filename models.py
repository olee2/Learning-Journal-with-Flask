import datetime

from peewee import *

DATABASE = SqliteDatabase("journal.db")

class Entry(Model):
    title = CharField(unique=True)
    date = DateTimeField(default=datetime.datetime.now)
    time_spent = IntegerField()
    learned = TextField()
    resources = TextField()
    
    class Meta:
        database = DATABASE
        order_by = ("-timestamp",)



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
    
