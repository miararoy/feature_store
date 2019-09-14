import os
import json

from flask import Response
import connexion

from feature_store.warehouse import Warehouse
from feature_store.real_time_data import RTDB
from feature_store.catalog import Catalog
from feature_store.config import MDB_URL
from feature_store.feature_extraction import rt, warehouse
from flow.flow import get_single_flow

from feature_store.logger import Logger

log = Logger("app").get_logger()

# warehouse = Warehouse(url=PSG_URL)
# warehouse.create()

# rt = RTDB()
# rt.create()

catalog = Catalog(MDB_URL)


def publish(n_flows):
    for i in range(n_flows):
        q, u, t, p = get_single_flow()
        warehouse.insert("quotes", q)
        rt.insert("quotes", q)
        print(q)
        if u:
            warehouse.insert("users", u)
            rt.insert("users", u)
            print(u)
        if t:
            warehouse.insert("transactions", t)
            rt.insert("transactions", t)
            print(t)
        if p:
            warehouse.insert("policies", p)
            rt.insert("policies", p)
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

def extract():
    pass

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