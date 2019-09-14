import pandas as pd
import os
import urllib
from time import time
from datetime import datetime
import importlib
from uuid import UUID

from feature_store.catalog import Catalog
from feature_store.config import MDB_URL, PSG_URL, SCHEMA
from feature_store.warehouse import Warehouse
from feature_store.real_time_data import RTDB
from feature_store.file_handler import ArtifactHandler, load_etl

from feature_store.logger import Logger

log = Logger("FeatureExtraction").get_logger()

warehouse = Warehouse(url=PSG_URL)
warehouse.create()

rt = RTDB()
rt.create()

catalog = Catalog(MDB_URL)

base_path = "lib/etl"


class FeatureExtraction(object):
    
    def __init__(self, etl: str):
        if etl.endswith(".py"):
            self.Etl = load_etl(etl)
        else:
            path_to_feature_file = catalog.load("feature", etl)["path"]
            self.Etl = ArtifactHandler().load(path_to_feature_file)
        self._etl = etl

    def extract(self, query_id, is_serving=False, **serving_args)-> pd.core.frame.DataFrame:
        q = catalog.load("query", query_id)["query"]
        if is_serving:
            if "key" in serving_args and "value" in serving_args:
                q = q.replace(SCHEMA, "main")
                data = rt.query(q, key=serving_args["key"], value=serving_args["value"])
            else:
                raise ValueError("Not using key, value in serving_args resuls is not premitted ATM")
        else:
            data = warehouse.query(q)
        df = pd.DataFrame(data)
        df_extracted_features = self.Etl(df).extract()
        return df_extracted_features.to_dict(orient="records")
        
    def save(self, name:str=str(int(time()))):
        artifact_path = os.path.join(base_path, "{}.py".format(name))
        save_path = ArtifactHandler(artifact=self._etl).save(artifact_path)
        metadata = {"path": save_path, "save_time": datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")}
        save_id = catalog.save("X", "feature", metadata)
        return save_id