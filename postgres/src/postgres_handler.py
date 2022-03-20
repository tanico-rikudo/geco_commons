import psycopg2
from psycopg2.extras import DictCursor, execute_values

PostgresHandlerQueryMolts = {
    "insertOhlcv": "INSERT INTO ohlcv ({0}) VALUES %s;"
}


class PostgresUtil:

    def __init__(self, PostgresHandler, logger):
        self.dao = PostgresHandler
        self._logger = logger
        

    def insert_ohlcv(self, ohlcv_dict):
        datas = ohlcv_dict.to_dict(orient='record')
        values=[tuple(p.values()) for p in datas]
        keys=list(datas[0].keys())
        
        # Key check
        essential_key_list = set({"datetime", "open", "high", "low", "close", "volume", "symbol"})
        assert essential_key_list == set(keys), f'Must be match ohlcv  table leys. You={keys}, Table={essential_key_list}'
        
        # Make key list
        key_names = ""
        length = len(keys)
        for i, _name in enumerate(keys):
            key_names+=_name
            if i < length-1:
                key_names+=","
            
        query = PostgresHandlerQueryMolts.get("insertOhlcv").format(key_names)
        
        self.dao.insert(query,values)


class PostgresHandler:

    def __init__(self, config):
        self.host = config.get('POSTGRES_HOST')
        self.port = config.get('POSTGRES_PORT')
        self.db_name = config.get('POSTGRES_NAME')
        self.db_user = config.get('POSTGRES_USERNAME')
        self.cursor_mode = config.getboolean('POSTGRES_SERVERCURSORMODE')
        self.db_pw = config.get('POSTGRES_PASSWORD')

    def get_conn(self):
        """ Get connection

        Returns:
            psycopg2.Connection: Or None
        """
        try:
            conn = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_pw,
                host=self.host,
                port=self.port)
        except Exception as e:
            conn = None

        return conn

    def get_cursor(self, conn, cursor_mode=None):
        """ Get cursor

        Args:
            conn (psycopg2.Connection): _description_
            cursor_mode (psycopg2.cursor, optional): If set, cursor is declared in Server side.
                                                    It makes local be more light. Defaults to None.

        Returns:
            cursor object: Or None
        """
        cur = None
        try:
            cursor_mode = self.cursor_mode if cursor_mode is None else cursor_mode
            cursor_name = 'named_cursor' if cursor_mode is True else None
            cur = conn.cursor(name=cursor_name, cursor_factory=DictCursor)
        except Exception as e:
            cur = None

        return cur

    def fetch(self, sql):
        cur = self.get_cursor(self.get_conn(), cursor_mode=self.cursor_mode)
        cur.execute(sql)
        result = []
        while True:
            row = cur.fetchone()
            if row is None:
                break
            result.append(dict(row))
            
        return result

    def insert(self, query, params):
        conn = self.get_conn()
        # cur = self.get_cursor(conn, cursor_mode=self.cursor_mode)
        cur = self.get_cursor(conn, cursor_mode=False)
        ret = execute_values(cur, query, params)
        conn.commit()
