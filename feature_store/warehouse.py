from feature_store.psg_client import PSClient
from feature_store.config import Tables, Schemas, SCHEMA
from feature_store.utils import generate_key_value_query, pd


class Warehouse(object):
    """warehouse db that handles "cold" data
    """
    def __init__(self, url):
        """init the db client
        """
        self.client = PSClient(url=url)

    def create(self):
        """creates tables and schemas
        """
        self.client.execute(Schemas.SCHEMA["create"])
        tables = [Tables.USERS, Tables.QUOTES, Tables.POLICIES, Tables.TRANSACTIONS]
        for table in tables:
            cmd = table["create"]
            self.client.execute(cmd)
    
    def insert(self, table: str, data: dict):
        """inserts to data to table

        Args:
            table(str): db table
            data(str): data to insert
        """
        insert_cmd = getattr(Tables,table.upper())["insert"]
        self.client.execute_prepared(
            insert_cmd, 
            data
        )
    
    def query(self, cmd):
        """query the database. runs cmd and wraps 
        
        Args:
            cmd(str): sql query
        
        Returns:
            df(array-like): record oriented dataframe
        """
        df = self.client.query(cmd)
        return df.to_dict(orient='records')
