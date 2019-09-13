from feature_store.psg_client import PSClient
from feature_store.config import Tables, Schemas, SCHEMA
from feature_store.utils import generate_key_value_query, pd

LOCAL_URL = "postgresql://postgres:mysecretpassword@localhost:5432/feature_store"

class Warehouse(object):
    def __init__(self, url):
        self.client = PSClient(url=url)

    def create(self):
        self.client.execute(Schemas.SCHEMA["create"])
        tables = [Tables.USERS, Tables.QUOTES, Tables.POLICIES, Tables.TRANSACTIONS]
        for table in tables:
            cmd = table["create"]
            self.client.execute(cmd)
    
    def insert(self, table: str, data: dict):
        insert_cmd = getattr(Tables,table.upper())["insert"]
        self.client.execute_prepared(
            insert_cmd, 
            data
        )
    
    def query(self, cmd):
        df = self.client.query(cmd)
        df["creation_date"] = df["creation_date"].astype(str)
        return df.to_dict(orient='records')


if __name__ == "__main__":
    data = {"quote_id": "42c2374d-dc94-4344-ae32-2a3e035ffdf4", "is_binded": False, "is_paid": True, "binding_date": None, "user_id": None, "creation_date": "2019-09-14 01:00:55.923273", "quote_data": {"type": "owner", "device": "mobile"}}
    wrhs = Warehouse(LOCAL_URL)
    wrhs.create()
    wrhs.insert("quotes", data)
    res = wrhs.query("""select * from {}.Users""".format(SCHEMA), "user_id", "9f3f88c1-7459-4235-8d94-c3507d144dda")
    print(res)