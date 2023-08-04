"""
    This file is a part of SQL DAL Maker project: https://sqldalmaker.sourceforge.net
    It demonstrates how to implement an interface DataStore in Python + SQLAlchemy.
    More about DataStore: https://sqldalmaker.sourceforge.net/preconfig.html#ds
    Recent version: https://github.com/panedrone/sqldalmaker/blob/master/src/resources/data_store_sqlalchemy.py

    Successfully tested with:
        - sqlite3 ---------------- built-in
        - postgresql ------------- pip install psycopg2
        - mysql+mysqlconnector --- pip install mysql-connector-python
        - cx_Oracle -------------- pip install cx_oracle

    Copy-paste it to your project and change it for your needs.
    Improvements are welcome: sqldalmaker@gmail.com

"""

import sqlalchemy.orm

from sqlalchemy import text


class OutParam:
    def __init__(self):
        self.value = None


class DataStore:

    def begin(self): pass

    def commit(self): pass

    def rollback(self): pass

    # ORM-based raw-SQL helpers

    def get_one_raw(self, cls, params=None):
        """
        :param cls: a model class containing static field SQL
        :param params: a tuple of SQL params
        :return: a model object or error string
        """
        pass

    def get_all_raw(self, cls, params=None) -> []:
        """
        :param cls: a model class containing static field SQL
        :param params: a tuple of SQL params
        :return: an array of model objects
        """
        pass

    # ORM-based helpers

    def get_query(self, cls):
        """
        :param cls: a model class
        """
        pass

    def filter(self, cls, params: dict):
        """
        :param cls: a model class
        :param params: dict of named filter params
        :return: a QuerySet
        """
        pass

    def delete_by_filter(self, cls, params: dict) -> int:
        """
        delete_by_filter
        :param cls: a model class
        :param params: dict of named filter params
        :return: amount of rows affected
        """
        pass

    def update_by_filter(self, cls, data: dict, params: dict) -> int:
        """
        update_by_filter
        :param cls: a model class
        :param data: dict of column-value to update
        :param params: dict of filter params
        :return: amount of rows affected
        """
        pass

    # ORM-based CRUD

    def create_one(self, entity) -> None:
        """
        create_one
        :param entity: a model object or serializer object
        :return: None
        """
        pass

    def read_all(self, cls) -> []:
        """
        :param cls: a model class
        :return: a list model objects
        """
        pass

    def read_one(self, cls, pk: dict):
        """
        :param cls: a model class
        :param pk: primary key as a dict of column-value pairs
        :return: a model object
        """
        pass

    def update_one(self, cls, data: dict, pk: dict) -> int:
        """
        update_one
        :param cls: model class
        :param data: dict of column-value to update
        :param pk: primary key as a dict of column-value pairs
        :return: int, amount of rows affected
        """
        pass

    def delete_one(self, cls, pk: dict) -> int:
        """
        :param cls: model class
        :param pk: primary key as a dict of column-value pairs
        :return: int, amount of rows affected
        """
        pass

    # ORM-based methods for raw-SQL

    # === raw-SQL INSERT is not used with sqlalchemy: def insert_row(self, sql, params, ai_values): pass

    def exec_dml(self, sql, params) -> int:
        """
        :param sql: str, SQL statement
        :param params: dict, optional, SQL parameters
        :return: int: amount of affected rows
        """
        pass

    def query_scalar(self, sql, params):
        """
        :param sql: str, SQL statement
        :param params: dict, optional, SQL parameters
        :return single scalar value
        :raise Exception: if amount of fetched rows != 1
        """
        pass

    def query_all_scalars(self, sql, params) -> []:
        """
        :param sql: str, SQL statement
        :param params: dict, optional, SQL parameters
        :return array of scalar values
        """
        pass

    def query_row(self, sql, params):
        """
        :param sql: str, SQL statement
        :param params: dict, optional, SQL parameters
        :return single fetched row or error string
        """
        pass

    def query_all_rows(self, sql, params, callback):
        """
        :param sql: str, SQL statement
        :param params: dict, optional, SQL parameters.
        :param callback: Ð° function delivering fetched rows to caller
        :return: None
        """
        pass


Base = sqlalchemy.orm.declarative_base()

Column = sqlalchemy.Column
ForeignKey = sqlalchemy.ForeignKey

SmallInteger = sqlalchemy.SmallInteger
Integer = sqlalchemy.Integer
BigInteger = sqlalchemy.BigInteger

Float = sqlalchemy.Float

DateTime = sqlalchemy.DateTime

String = sqlalchemy.String
Boolean = sqlalchemy.Boolean
LargeBinary = sqlalchemy.LargeBinary


def create_ds(session: sqlalchemy.orm.Session) -> DataStore:  # factory
    return _DS(session)  # session is constructed by "scoped_session" factory


class _DS(DataStore):
    class EngineType:
        sqlite3 = 1
        mysql = 2
        postgresql = 3
        oracle = 4

    def __init__(self, session: sqlalchemy.orm.Session):
        self.conn = None
        self.transaction = None
        self.engine = None
        self.engine_type = self.EngineType.sqlite3
        self.session: sqlalchemy.orm.session = session

    def begin(self):
        if self.transaction is None:
            # https://docs.sqlalchemy.org/en/14/orm/session_transaction.html
            self.session.begin()
            return
        # https://docs.sqlalchemy.org/en/14/core/connections.html
        self.transaction = self.conn.begin()

    def commit(self):
        if self.transaction is None:
            self.session.commit()
            return
        # https://docs.sqlalchemy.org/en/14/core/connections.html
        self.transaction.commit()
        self.transaction = None

    def rollback(self):
        if self.transaction is None:
            # https://docs.sqlalchemy.org/en/14/orm/session_basics.html
            self.session.rollback()
            return
        # https://docs.sqlalchemy.org/en/14/core/connections.html
        self.transaction.rollback()
        self.transaction = None

    def get_all_raw(self, cls, params=None) -> []:
        # https://stackoverflow.com/questions/17972020/how-to-execute-raw-sql-in-flask-sqlalchemy-app
        # user = session.query(User).from_statement(
        #     text("""SELECT * FROM users where name=:name""")
        # ).params(name="ed").all()

        # query = self.ds.engine.execute(GroupExModel.SQL) # it returns an array of tuples
        # return query.all()
        """
        get_all_raw
        :param cls: An __abstract_ model class or plain DTO class containing a static field "SQL"
        :param params: [] the values of SQL params
        :return: [dict]: an array of dict like [{'g_id': 21, 'g_name': 'Project 1'}, {'g_id': 22, 'g_name': 'Project 2']
        """
        # rows = self.engine.execute(cls.SQL)  # .fetchall()
        # performs -->
        # connection = self.connect(close_with_result=True) ---- no need because of connected
        if params is None:
            params = []

        # raw_conn.row_factory = sqlite3.Row # not working on python 3.11
        # raw_conn.row_factory = dict_factory  # not working on python 3.11

        exec_res = self._exec(cls.SQL, params)
        try:
            raw_cursor = exec_res.cursor
            col_names = [tup[0] for tup in raw_cursor.description]
            res = []
            for row in exec_res:
                row_values = [i for i in row]
                row_as_dict = dict(zip(col_names, row_values))
                r = cls(**dict(row_as_dict))
                res.append(r)
            return res
        finally:
            exec_res.close()

    def get_one_raw(self, cls, params=None):
        rows = self.get_all_raw(cls, params)
        if len(rows) == 1:
            return rows[0]
        if len(rows) == 0:
            return 'No rows'
        return 'More than 1 row exists'

    def get_query(self, cls):
        return self.session.query(cls)

    def filter(self, cls, params: dict):
        return self.session.query(cls).filter_by(**params)

    def delete_by_filter(self, cls, params: dict) -> int:
        found = self.filter(cls, params)
        #  :return: the count of rows matched as returned by the database's
        #           "row count" feature.
        return found.delete()  # found is a BaseQuery, no fetch!

    def update_by_filter(self, cls, data: dict, params: dict) -> int:
        found = self.filter(cls, params)
        return found.update(values=data)  # found is a BaseQuery, no fetch!

    def create_one(self, entity) -> None:
        self.session.add(entity)  # return None
        self.session.flush()

    def read_all(self, cls):
        return self.session.query(cls).all()

    def read_one(self, cls, pk: dict):
        return self.session.query(cls).get(pk)

    def update_one(self, cls, data: dict, pk: dict) -> int:
        rc = self.update_by_filter(cls, data, pk)
        self.session.flush()
        return rc

    def delete_one(self, cls, pk: dict) -> int:
        # found = self.read_one(cls, params) # found is an entity of class cls
        # self.session.delete(found)
        rc = self.delete_by_filter(cls, pk)  # no fetch!
        self.session.flush()
        return rc

    def _exec(self, sql, params):
        """
        :param sql:
        :param params:
        :return: <sqlalchemy.engine.cursor.LegacyCursorResult object at 0x00000243D83C5D00>
        """
        pp = tuple(params)
        txt = text(sql)  # don't use sqlalchemy.text(sql) with '%' as params
        return self.session.execute(txt, pp)

    def _exec_proc_pg(self, sql, params):
        out_params = []
        call_params = []
        for p in params:
            if isinstance(p, OutParam):
                call_params.append(p.value)
                out_params.append(p)
            else:
                call_params.append(p)
        cursor = self._exec(sql, call_params)
        try:
            if len(out_params) > 0:
                row0 = cursor.fetchone()
                i = 0
                for value in row0:
                    out_params[i].value = value
                    i += 1
        finally:
            cursor.close()

    def _exec_sp_mysql(self, sp, params):
        call_params = self._get_call_params(params)
        # https://stackoverflow.com/questions/45979950/sqlalchemy-error-when-calling-mysql-stored-procedure
        raw_conn = self.session.connection()
        try:
            with raw_conn.cursor() as cursor:
                result_args = cursor.callproc(sp, call_params)
                for p in params:
                    if isinstance(p, list) and callable(p[0]):
                        i = 0
                        for result in cursor.stored_results():
                            callback = p[i]
                            self._fetch_all(result, callback)
                            i += 1
                        break
                self._assign_out_params(params, result_args)
        finally:
            raw_conn.close()

    def _query_sp_mysql(self, sp, on_result, params):
        call_params = self._get_call_params(params)
        # https://stackoverflow.com/questions/45979950/sqlalchemy-error-when-calling-mysql-stored-procedure
        raw_conn = self.session.connection()
        try:
            with raw_conn.cursor() as cursor:
                # result_args: https://pynative.com/python-mysql-execute-stored-procedure/
                result_args = cursor.callproc(sp, call_params)
                for result in cursor.stored_results():
                    on_result(result)
                self._assign_out_params(params, result_args)
        finally:
            raw_conn.close()

    def exec_dml(self, sql, params) -> int:
        sql = self._format_sql(sql)
        sp = self._get_sp_name(sql)
        if sp is None:
            cursor = self._exec(sql, params)
            try:
                return cursor.rowcount
            finally:
                cursor.close()
        if self.engine_type == self.EngineType.postgresql:
            self._exec_proc_pg(sql, params)  # sql!
        elif self.engine_type == self.EngineType.mysql:
            self._exec_sp_mysql(sp, params)  # sp!
        else:
            raise Exception('Not supported for this engine')
        return 0

    def query_scalar(self, sql, params):
        rows = self.query_all_scalars(sql, params)
        if len(rows) == 0:
            raise Exception('No rows')
        if len(rows) > 1:
            raise Exception('More than 1 row exists')
        if isinstance(rows[0], list):
            return rows[0][0]
        else:
            return rows[0]  # 'select get_test_rating(?)' returns just scalar value, not array of arrays

    def query_all_scalars(self, sql, params):
        sql = self._format_sql(sql)
        res = []
        sp = self._get_sp_name(sql)
        if sp is None:
            cursor = self._exec(sql, params)
            try:
                for row in cursor:
                    res.append(row[0])
                return res
            finally:
                cursor.close()
        if self.engine_type != self.EngineType.mysql:
            raise Exception('Not supported for this engine')

        def on_result(result):
            for row_values in result:
                res.append(row_values[0])

        self._query_sp_mysql(sp, on_result, params)
        return res

    def query_row(self, sql, params):
        rows = []
        self.query_all_rows(sql, params, lambda row: rows.append(row))
        if len(rows) == 1:
            return rows[0]
        if len(rows) == 0:
            return 'No rows'
        return 'More than 1 row exists'

    def query_all_rows(self, sql, params, callback):
        sql = self._format_sql(sql)
        sp = self._get_sp_name(sql)
        if sp is None:
            cursor = self._exec(sql, params)
            try:
                for row in cursor:
                    callback(row)
                return
            finally:
                cursor.close()
        if self.engine_type != self.EngineType.mysql:
            raise Exception('Not supported for this engine')
        self._query_sp_mysql(sp, lambda result: self._fetch_all(result, callback), params)

    def _format_sql(self, sql):
        if self.engine_type == self.EngineType.sqlite3:
            return sql
        return sql.replace("?", "%s")

    @staticmethod
    def _fetch_all(cursor, callback):
        # https://stackoverflow.com/questions/34030020/mysql-python-connector-get-columns-names-from-select-statement-in-stored-procedu
        # https://kadler.github.io/2018/01/08/fetching-python-database-cursors-by-column-name.html#
        for r in cursor:
            # https://stackoverflow.com/questions/1958219/how-to-convert-sqlalchemy-row-object-to-a-python-dict
            # How to convert SQLAlchemy row object to a Python dict?
            row = dict(r)
            # i = 0
            # for d in result.description:
            #     col_name = d[0]
            #     value = r[i]
            #     row[col_name] = value
            #     i = i + 1
            callback(row)

    @staticmethod
    def _get_sp_name(sql):
        parts = sql.split()
        if len(parts) >= 2 and parts[0].strip().lower() == "call":
            name = parts[1]
            end = name.find("(")
            if end == -1:
                return name
            else:
                return name[0:end]
        return None

    @staticmethod
    def _get_call_params(params):
        """
        COMMENT FROM SOURCES OF MySQL Connector => cursor.py:

        For OUT and INOUT parameters the user should provide the
        type of the parameter as well. The argument should be a
        tuple with first item as the value of the parameter to pass
        and second argument the type of the argument.
        """
        call_params = []
        for p in params:
            if isinstance(p, OutParam):
                call_params.append(p.value)
            elif isinstance(p, list) and callable(p[0]):
                pass  # MySQL SP returning result-sets
            else:
                call_params.append(p)
        return call_params

    @staticmethod
    def _assign_out_params(params, result_args):
        for i in range(len(params)):
            if isinstance(params[i], OutParam):
                params[i].value = result_args[i]
