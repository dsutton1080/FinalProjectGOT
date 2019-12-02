import sqlite3
from config import Config

conf = Config()
dbfile = "dev2.db" if conf.TEST_USER_POPULATED_DB else "dev.db"
conn = sqlite3.connect(dbfile)
curs = conn.cursor()