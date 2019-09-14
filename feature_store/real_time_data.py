import sqlite3

from time import time 

from feature_store.config import Tables, Schemas, SCHEMA
from feature_store.utils import generate_key_value_query, pd

class RTDB(object):
    class _RTDB(object):
        """Real Time DataBase (RTDB) is an in memory sql db that handles "warm" data
        """
        def __init__(self):
            """init the db in mem
            """
            self.conn = sqlite3.connect(":memory:", check_same_thread=False)
            self.curosor: sqlite3.Cursor = self.conn.cursor()

        def create(self):
            """creates tables and schemas
            """
            tables = [t for t in dir(Tables) if not t.startswith('__') and not callable(getattr(Tables,t))]
            for table in tables:
                cmd = getattr(Tables,table)["create_rt"]
                self.curosor.execute(cmd)

        def insert(self, table: str, data: dict):
            """inserts to data to table

            Args:
                table(str): db table
                data(str): data to insert
            """
            insert_data = tuple(data[c] for c in getattr(Tables,table.upper())["rt_values"])
            insert_cmd = getattr(Tables,table.upper())["insert_rt"]
            self.curosor.execute(
                insert_cmd, 
                insert_data
            )
            self.conn.commit()
        
        def query(self, cmd, key, value):
            """query the database. runs cmd and wraps a where clause 
            key=value
            
            Args:
                cmd(str): sql query 
                key(str): index key for where clause
                value("str): index value for where clause
            
            Returns:
                df(array-like): record oriented dataframe
            """
            df = pd.read_sql_query(generate_key_value_query(cmd, key, value), self.conn)
            return df.to_dict(orient='records')
    
    instance = None

    def __new__(
        cls
    ):
        if RTDB.instance is None:
            RTDB.instance = RTDB._RTDB()
        return RTDB.instance