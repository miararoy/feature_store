import os
import urllib
import importlib
import pandas as pd
from time import time
from datetime import datetime
from uuid import UUID

from feature_store.catalog import Catalog
from feature_store.config import MDB_URL, PSG_URL, SCHEMA
from feature_store.warehouse import Warehouse
from feature_store.real_time_data import RTDB
from feature_store.file_handler import EtlArtifactHandler, load_etl
from feature_store.utils import is_schema_equal, df_schema
from feature_store.logger import Logger

log = Logger("FeatureExtraction").get_logger()

warehouse = Warehouse(url=PSG_URL)
warehouse.create()

rt = RTDB()
rt.create()

catalog = Catalog(MDB_URL)

ETL_BASE_PATH = "lib/etl"

class FeatureExtraction(object):
    """class that handles feature extractions, running db queries and
    transformations

    """
    
    def __init__(self, etl: str):
        """init class with feature extractions logic

        Args:
            etl(str): etl(feature) id or a path (local/git) to .py file
        """
        if etl.endswith(".py"): # FILE ON GIT
            self.Etl = load_etl(etl)
        else: # ETL ID
            path_to_feature_file = catalog.load("feature", etl)["path"]
            self._schema = catalog.load("feature", etl)["etl_schema"]
            self.Etl = EtlArtifactHandler().load(path_to_feature_file)
        self._etl = etl

    def extract(self, query_id, is_serving=False, **serving_args)-> pd.core.frame.DataFrame:
        """query database and do trasnformations

        Args:
            query_id(str): query object id
            is_serving(bool): should extract data from warehouse or realtime
            serving_args(dict): additional query args
        
        Returns:
            df_extracted_features(array-like): an array of dict
        """
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
        if is_serving:
            if not is_schema_equal(self._schema, df_schema(df_extracted_features)):
                raise ValueError("feature and data schema not equal")
        else:
            self._schema = df_schema(df_extracted_features)
        return df_extracted_features.to_dict(orient="records")
        
    def save(self, name:str=str(int(time()))):
        """save etl to catalog

        Args:
            name(str): name of etl pipeline, defatult to time in sec

        Returns:
            save_id(str): id
        """
        artifact_path = os.path.join(ETL_BASE_PATH, "{}.py".format(name))
        save_path = EtlArtifactHandler(artifact=self._etl).save(artifact_path)
        metadata = {
            "path": save_path, 
            "save_time": datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f"),
            "etl_schema": self._schema
        }
        save_id = catalog.save("X", "feature", metadata)
        return save_id