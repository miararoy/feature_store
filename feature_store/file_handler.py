from os import path, makedirs
from sklearn.externals import joblib
import pickle
import importlib

from feature_store.logger import Logger

log = Logger("ArtifactHandler").get_logger()

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
        try:
            print("trying to pickle {} of type".format(
                self.artifact
            ))
            with open(path, 'wb') as artifcat_file:
                joblib.dump(
                    self.artifact,
                    artifcat_file,
                )
        except pickle.PicklingError as e:
            log.error("Cannot picke model at {p} due to {e}".format(p=path, e=e)) 
        return path


    def load(
        self,
        path: str,
    ):
        with open(path, 'rb') as model_file:
            return joblib.load(model_file)



