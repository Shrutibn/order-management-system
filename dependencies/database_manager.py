import os
import threading

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import sys


class DatabaseManager:

    def __init__(self):
        self.threadLocal = threading.local()

    def get_db(self, con):
        conn_pool = getattr(self.threadLocal, 'conn_pool', {})
        try:
            if con in conn_pool and conn_pool[con] is not None:
                return Session(conn_pool[con], future=True)
            else:
                rconn = self.reset_db_conn(con)
                return rconn

        except Exception as exception:
            exc_obj = sys.exc_info()
            exc_type = exc_obj[0]
            exc_tb = exc_obj[2]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            exception_string = str(exc_type) + " & " + str(fname) + " & " + str(exc_tb.tb_lineno)
            print("An exception has occurred in the DB connection over-all as : {0}, at : {1}".format(exception, exception_string))

    def reset_db_conn(self, con_key):
        conn = None
        conn_pool = getattr(self.threadLocal, 'conn_pool', {})
        try:
            if con_key in conn_pool and conn_pool[con_key] is not None:
                conn_pool[con_key].dispose()

        except Exception as e:
            exc_obj = sys.exc_info()
            exc_type = exc_obj[0]
            exc_tb = exc_obj[2]
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            exception_string = str(exc_type) + " & " + str(fname) + " & " + str(exc_tb.tb_lineno)
            print("An exception has occurred in the DB connection as : {0}, at : {1}".format(e, exception_string))

        for i in range(3):
            try:
                conn = create_engine(con_key)
                break

            except Exception as e:
                exc_obj = sys.exc_info()
                exc_type = exc_obj[0]
                exc_tb = exc_obj[2]
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                exception_string = str(exc_type) + " & " + str(fname) + " & " + str(exc_tb.tb_lineno)
                print("An exception has occurred in the DB connection as : {0}, at : {1}".format(e, exception_string))
                conn = None
                continue

        if conn is not None:
            print("created...{0} for {1}".format(id(conn), con_key))
            conn_pool[con_key] = conn
            self.threadLocal.conn_pool = conn_pool

        return Session(conn, future=True)

db_manager = DatabaseManager()