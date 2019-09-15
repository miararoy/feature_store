import os
import urllib
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



