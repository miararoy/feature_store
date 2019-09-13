from pymongo import MongoClient

from feature_store.logger import Logger

logger = Logger("MDBClient").get_logger()

class MDBClient:
    class _MDBClient(object):
        """basic client that connects to PS cluster

        """
        def __init__(
            self,
            url: str,
            keep_alive: bool,
        ):
            """initializes a connection from a url

            """
            self.url = url
            self.session = None
            self.endpoint = self.url.split('@')[1].split('/')[0]
            self.host = self.endpoint.split(',')
            self.db = self.url.split('@')[1].split('/')[1].split('?')[0]
            self.keep_alive = keep_alive

        def connect(
            self,
            force_close_old_connection=False,
        ):
            """connects to mongo using the mongo_db_url that is the initiialization

            Args:
                force_close_old_connection(bool): should old connection be closed

            Raises:
                Exception: when trying to override connection on same session without flag
                RuntimeError: when connection to mongo failes
            """
            try:
                if not self.session:
                    self.session = MongoClient(
                        self.url
                    )
                elif force_close_old_connection:
                    self.session.close()
                    self.session = MongoClient(
                        self.url
                    )
                else:
                    raise Exception(
                        "There is an open Session already, try using " +
                        "force_close_old_connection = True"
                    )
            except Exception as e:
                raise e
            except BaseException:
                raise RuntimeError("could not connect to mongo @ {h}:{p}".format(
                    h=self.host,
                ))
            finally:
                print("connected to DB: {db} @ {h}".format(
                    h=self.host,
                    db=self.db
                ))


        def get(
            self,
        ):
            if not self.session:
                self.connect()
            return self.session[self.db]

        
        def query(
            self,
            collection: str,
            q: dict,
        ):
            db = self.get()
            try:
                return list(db[collection].find(q))[0]
            except BaseException:
                raise RuntimeError(
                    "query {q} Failed to return from DB".format(
                        q=q
                    )
                )
            finally:
                if not self.keep_alive:
                    print("closing connection to db {db}".format(
                        db=db.name
                    ))
                    db.client.close()
        
        def insert(
            self,
            collection:str,
            obj: dict,
        ):
            db = self.get()
            return str(db[collection].insert_one(obj).inserted_id)
        

        def close(self,):
            db = self.get()
            print("closing connection to db {db}".format(
                db=db.name
            ))
            db.client.close()

    instance = None

    def __new__(
        cls,
        url,
        keep_alive=False,
    ):
        if MDBClient.instance is None:
            MDBClient.instance = MDBClient._MDBClient(url, keep_alive)
        else:
            logger.info("MDBClient object already initialized")
        return MDBClient.instance
