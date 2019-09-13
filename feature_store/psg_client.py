import os

import pandas as pd
import psycopg2
from sqlalchemy import create_engine

from feature_store.logger import Logger

logger = Logger("PSClient").get_logger()

class PSClient:
    class _PSClient(object):
        """basic client that connects to PS cluster

        """
        def __init__(
            self,
            url: str
        ):
            """initializes a connection
            """
            self.url = url
            self.database = os.path.split(self.url)[-1]
            self.engine = create_engine(self.url)
            self.conn = None
            self.curr = None

        def connect(self,):
            self.conn = psycopg2.connect(self.url)
            logger.info("connected to {}".format(self.database))
        
        def get_connection(self):
            """returns connection
            """
            self.connect()
            return self.conn

        def execute(
            self,
            cmd:str
        ):
            """will execute single command and commit the changes
            Args:
                cmd(str): list of commands
            """
            try:
                with self.get_connection() as conn:
                    with self.conn.cursor() as cur:
                        cur.execute(cmd)
                        cur.close()
                    conn.commit()
                logger.info("executed and commited: `{}`".format(cmd[:30]))
            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(error)
                self.get_connection().commit()

        def query(
            self,
            cmd: str,
        ):
            """will execute query and return pd.DataFrame

            Args:
                cmd(str): select query to execute
            """ 
            if cmd.strip()[:6].lower() == "select":
                return pd.read_sql_query(cmd, self.engine)
            else:
                raise ValueError("only select commands are allowed, not {}, use .execute() instead") 

        def execute_prepared(
            self,
            prepared_statement: str,
            cmd,
        ):
            """will execute multiple commands and commit the changes
            Args:
                cmd(list): list of commands
            """
            try:
                with self.get_connection() as conn:
                    with self.conn.cursor() as cur:
                        if isinstance(cmd, list):
                            cur.executemany(prepared_statement,cmd)
                        elif isinstance(cmd,dict):
                            cur.execute(prepared_statement,cmd)
                        is_executed = cur.statusmessage == 'INSERT 0 1'
                    conn.commit()
                    if is_executed:
                        logger.info("executed and commited: `{}` rows".format(len(cmd)))
                        return True
                    else:
                        logger.warn("could not execute cmd properly. Reason == [{}]".format(cur.statusmessage))
                        return False
            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(error)
                logger.error(cmd)
                return False

        def close_connection(self,):
            """closes connection to database
            """
            logger.info("closing connection to {}".format(self.database))
            self.conn.close()
            logger.info("closed connection to {} successfuly".format(self.database))
    
    instance = None

    def __new__(
        cls,
        url
    ):
        if PSClient.instance is None:
            PSClient.instance = PSClient._PSClient(url)
        else:
            logger.info("PSClient object already initialized")
        return PSClient.instance
