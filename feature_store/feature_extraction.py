import pandas as pd
from os import path
from time import time
import importlib

from feature_store.catalog import Catalog
from feature_store.config import MDB_URL, PSG_URL, SCHEMA
from feature_store.warehouse import Warehouse
from feature_store.real_time_data import RTDB
from feature_store.file_handler import ArtifactHandler

from feature_store.logger import Logger

log = Logger("FeatureExtraction").get_logger()

warehouse = Warehouse(url=PSG_URL)
warehouse.create()

rt = RTDB()
rt.create()

catalog = Catalog(MDB_URL)

base_path = "lib/etl"

def load_etl(
    path: str,
):
    spec = importlib.util.spec_from_file_location(
        name='etl',
        location=path
    )
    etl = importlib.util.module_from_spec(
        spec
    )
    spec.loader.exec_module(etl)
    return etl.Etl

class FeatureExtraction(object):
    
    def __init__(self, path_to_etl_file):
        self.path_to_etl_file = path_to_etl_file
        self.Etl = load_etl(self.path_to_etl_file)

    def extract_train(self, query_id)-> pd.core.frame.DataFrame:
        q = catalog.load("query", query_id)["query"]
        data = warehouse.query(q)
        df = pd.DataFrame.from_dict(data, orient="records")
        df_extracted_features = self.Etl(df).extract()
        return df_extracted_features.to_dict(orient="records")
        
    def save(self, name:str=str(int(time()))):
        artifact_path = path.join(base_path, "{}.joblib".format(name))
        save_path = ArtifactHandler(artifact=self.Etl).save(artifact_path)
        return save_path


        
        
        # if self.Etl.schema_equals(df):
        #     # DO Train

        # else:
        #     raise ValueError("schema mismatch between data and etl")
    

        
