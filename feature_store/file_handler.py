import os
import urllib
import pickle
import joblib
import importlib
from time import time
from os import path, makedirs

from feature_store.logger import Logger

log = Logger("ArtifactHandler").get_logger()


def _load_etl(path:str):
    """reads a local .py file to Etl module

    Args:
        path(str): path to local .py etl file

    Returns:
        Etl(class): Etl class
    """
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
    """loads etl url to module

    Args(url): 
        url(str): path to .py etl file, web or local
    
    Returns:
        Etl(class): Etl class
    """
    if url.startswith("http"):
        if urllib.request.urlopen(url).status == 200:
            path = os.path.join("/tmp", "{}.py".format(str(int(time()))))
            urllib.request.urlretrieve(url, path)
            return _load_etl(path)
        else:
            raise urllib.error.URLError("cannot access url at: {}".format(url))
    else:
        return _load_etl(url)

def load_model(
    url: str,
):
    if url.startswith("http"):
        if urllib.request.urlopen(url).status == 200:
            path = os.path.join("/tmp", "{}.py".format(str(int(time()))))
            urllib.request.urlretrieve(url, path)
        else:
            raise urllib.error.URLError("cannot access url at: {}".format(url))
    spec = importlib.util.spec_from_file_location(
        name='model',
        location=path
    )
    model = importlib.util.module_from_spec(
        spec
    )
    spec.loader.exec_module(model)
    return model.Model


class ArtifactHandler(object):
    def __init__(
        self, 
        artifact=None,
    ):
        self.etl = artifact
        self.path = None


    def save(
        self,
        path=None,
    ):  
        self.path = path
        try:
            out = self.etl.etl
            print("trying to pickle {x} of type {xx}".format(
                x=out,
                xx=type(out)
            ))
            with open(self.path, 'wb') as model_file:
                joblib.dump(
                    out,
                    model_file,
                )
            return self.path
        except pickle.PicklingError as e:
            print("Cannot picke model at {p} due to {e}".format(p=self.path, e=e)) 
            return self.path


    def load(
        self,
        path: str,
    ):
        with open(path, 'rb') as model_file:
            return joblib.load(model_file)


class EtlArtifactHandler(object):
    """handles the saving and loading of ETL artifacts (ATM as .py files)
    """
    def __init__(
        self, 
        artifact=None,
    ):
        """init the ArtifactHandler with py artifact

        Args:
            artifact(file): py transformations etl file
        """
        self.artifact = artifact

    def save(
        self,
        path: str,
    ):  
        """saves artifact to path

        Args: 
            path(str): path to save artifact
        """
        urllib.request.urlretrieve(self.artifact, path)
        return path


    def load(
        self,
        path: str
    ):
        """loads artifact from path

        Args:
            path(str): artifact to load path from
        """
        return _load_etl(path)



