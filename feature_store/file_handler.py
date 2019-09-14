from os import path, makedirs
# from sklearn.externals import joblib
import joblib
import pickle
import urllib
import os
from time import time
import importlib

from feature_store.logger import Logger

log = Logger("ArtifactHandler").get_logger()


def _load_etl(path:str):
    spec = importlib.util.spec_from_file_location(
        name='etl',
        location=path
    )
    etl = importlib.util.module_from_spec(
        spec
    )
    spec.loader.exec_module(etl)
    return etl.Etl

def load_etl(
    url: str,
):
    print(url)
    if url.startswith("http"):
        if urllib.request.urlopen(url).status == 200:
            path = os.path.join("/tmp", "{}.py".format(str(int(time()))))
            urllib.request.urlretrieve(url, path)
            return _load_etl(path)
        else:
            raise urllib.error.URLError("cannot access url at: {}".format(url))
    else:
        return _load_etl(url)


class ArtifactHandler(object):
    def __init__(
        self, 
        artifact=None,
    ):
        self.artifact = artifact

    def save(
        self,
        path,
    ):  
        # try:
        #     print("trying to pickle {} of type {}".format(
        #         self.artifact, type(self.artifact)
        #     ))
        #     with open(path, 'wb') as artifcat_file:
        #         try:
        #             joblib.dump(self.artifact, artifcat_file)
        #             log.info("GOT PICKLE")
        #         except pickle.PicklingError as e:
        #             log.error("NO PICKLE "+str(e))
        #         joblib.dump(
        #             self.artifact,
        #             artifcat_file,
        #         )
        # except pickle.PicklingError as e:
        #     log.error("Cannot picke model at {p} due to {e}".format(p=path, e=e)) 
        urllib.request.urlretrieve(self.artifact, path)
        return path


    def load(
        self,
        path: str,
    ):
        return _load_etl(path)
        # with open(path, 'rb') as model_file:
        #     return joblib.load(model_file)



