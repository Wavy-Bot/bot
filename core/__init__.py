from core import database

# NOTE(Robert): This is here because it only gets called 1 time, when I put it in the __init__ of
#               the database.py file it would call it multiple times which is not what I want.

database.init_db()
