from urllib.parse import urlparse

from bson import ObjectId

from feature_store.config import CatalogConstants
from feature_store.logger import Logger
from feature_store.mdb_client import MDBClient


log = Logger("catalog").get_logger()

def _mask_uri(uri:str)-> str:
    """
    Args:
        uri(str): database uris

    Returns:
        parsed(str): masked uri
    """
    return urlparse(uri)._replace(
        netloc="{}:{}@{}".format(urlparse(uri).username, "******", urlparse(uri).hostname)
    ).geturl()


class Catalog(object):
    def __init__(
        self,
        db_url: str,
    ):
        """ initiates catalog and collection for storing features and
        queries
        Args:
            db_url(str): mongodb url
        """
        self.db_url = _mask_uri(db_url)
        self.client = MDBClient(db_url)
        self.db = self.client.get()
        
        self._query_collection = self.db[CatalogConstants.catalog_collections["query"]]
        self._feature_collection = self.db[CatalogConstants.catalog_collections["feature"]]
        self._model_collection = self.db[CatalogConstants.catalog_collections["model"]]
        log.info("successfuly got collections: [{}]".format(
            list(CatalogConstants.catalog_collections.values())
        ))


    def save(self, dev_id: str, data_type: str, data: dict):
        """
        Args:
            def_id(str): dev identifier
            data_type(str): feature, query or model object
            data(dict): catalog data
        Returns:
            obj_id(str): catalog object id
        """
        if data_type in CatalogConstants.catalog_collections.values():
            collection = CatalogConstants.catalog_collections[data_type]    
            obj = {**{"dev_id": dev_id}, **data}
            print(obj)
            obj_id = self.client.insert(
                collection=collection,
                obj=obj
            )
            log.info("developer {} successfuly inserted {} to {}".format(dev_id, obj_id, collection))
            return obj_id
        else:
            log.error("data_type does not match any collection on: [{}]".format(CatalogConstants.catalog_collections.values()))


    def load(self, data_type: str, obj_id:str):
        """
        Args:
            data_type(str): feature, query or model
            obj_id(str): catalog object id

        Returns:
            query(dict): catalog object
        """
        if data_type in CatalogConstants.catalog_collections.values():
            collection = CatalogConstants.catalog_collections[data_type]
            if isinstance(obj_id, str):
                _id = ObjectId(obj_id)
            elif isinstance(obj_id, ObjectId):
                _id = obj_id
            else:
                raise TypeError("obj_id type error, should be ObjectId or str")
            q = {
                "_id": _id
            }
            return self.client.query(collection=collection, q=q)
