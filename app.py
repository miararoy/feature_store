import os
import json

from flask import Response
import connexion

from feature_store.warehouse import Warehouse
from feature_store.real_time_data import RTDB
from feature_store.catalog import Catalog
from feature_store.config import SCHEMA
from flow.flow import get_single_flow

from feature_store.logger import Logger

log = Logger("app").get_logger()

LOCAL_URL = "postgresql://postgres:mysecretpassword@localhost:5432/feature_store"
LOCAL_MONGO = 'mongodb://root:root@0.0.0.0:27017/admin'


if os.getenv("DATABASE_URL"):
    psg_url = os.getenv("DATABASE_URL")
else:
    log.warn("Using local email since DATABASE_URL env was not found")
    psg_url = LOCAL_URL

if os.getenv("MONGO_URL"):
    mongo_url = os.getenv("MONGO_URL")
else:
    log.warn("Using local email since MONGO_URL env was not found")
    mongo_url = LOCAL_MONGO

warehouse = Warehouse(url=psg_url)
warehouse.create()

data = {"user_id": "66bedeae-e440-42e2-a3c2-908f6a9c4578", "creation_date": "2019-09-14 01:18:53.152790", "name": "Theophile Towne", "address": "71173 Price Island Metzstad, MI 96616"}
warehouse.insert("users", data)
res = warehouse.query("""select * from {}.Users""".format(SCHEMA))
print(res)

rt = RTDB()
rt.create()
rt.insert("users", data)


catalog = Catalog(mongo_url)


def publish(n_flows):
    for i in range(n_flows):
        q, u, t, p = get_single_flow()
        warehouse.insert("quotes", q)
        rt.insert("quotes", q)
        print(q)
        if u:
            warehouse.insert("users", u)
            print(u)
        if t:
            warehouse.insert("transactions", t)
            print(t)
        if p:
            warehouse.insert("policies", p)
            print(p)
    return Response(status=200, response=json.dumps({"msg": "created {} flows".format(n_flows)}))

def query_train(query, save):
    try:
        data = warehouse.query(query["query"])
        print(data)
    except:
        return Response(status=500, response=json.dumps({"msg": "failed fetching data"}))
    if save:
        query_id = catalog.save("roy", "query", query)
    else:
        query_id = None
    return Response(
        status=200, 
        response=json.dumps(
            {
                "query_id": query_id,
                "data": data
            }
        )
    )

def query_realtime(query):
    try:
        q = catalog.load("query", query["query_id"])["query"].replace(SCHEMA, "main")
        data = rt.query(q, query["key"], query["value"])
    except:
        return Response(status=500, response=json.dumps({"msg": "failed fetching data"}))
    return Response(
        status=200, 
        response=json.dumps(
            {
                "data": data
            }
        )
    )


if __name__ == "__main__":
    app = connexion.FlaskApp(
        __name__,
        port=int(os.environ.get("PORT") or 9090),
        specification_dir='swagger/'
    )
    app.add_api(
        'swagger.yaml',
        arguments={'title': 'feature_store'}
    )
    app.run()     