import sqlite3

from time import time 

from feature_store.config import Tables, Schemas, SCHEMA
from feature_store.utils import generate_key_value_query, pd

class RTDB(object):
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.curosor: sqlite3.Cursor = self.conn.cursor()

    def create(self):
        tables = [t for t in dir(Tables) if not t.startswith('__') and not callable(getattr(Tables,t))]
        for table in tables:
            cmd = getattr(Tables,table)["create_rt"]
            self.curosor.execute(cmd)

    def insert(self, table: str, data: dict):
        insert_data = tuple(data[c] for c in getattr(Tables,table.upper())["rt_values"])
        insert_cmd = getattr(Tables,table.upper())["insert_rt"]
        self.curosor.execute(
            insert_cmd, 
            insert_data
        )
        self.conn.commit()
    
    def query(self, cmd, key, value):
        df = pd.read_sql_query(generate_key_value_query(cmd, key, value), self.conn)
        return df.to_dict(orient='records')



if __name__ == "__main__":
    data = {"user_id": "9f3f88c1-7459-4235-8d94-c3507d144dda", "creation_date": "2019-09-13 16:30:38.248571", "name": "Ima Nikolaus", "address": "8756 Jaiden Station Lockmanland, CO 60674"}
    rtdb = RTDB()
    rtdb.create()
    rtdb.insert("users", data)
    res = rtdb.query("""select * from main.Users""", "user_id", "9f3f88c1-7459-4235-8d94-c3507d144dda")
    print(res)