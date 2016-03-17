import MySQLdb
import hashlib
import config


class Database:

    def __init__(self):
        self.host = config.mysql_host
        self.user = config.mysql_user
        self.password = config.mysql_pass
        self.db = config.mysql_db
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
        self.cursor = self.connection.cursor()

    def execute(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Database:
            self.connection.rollback()

    def query(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)

        return cursor.fetchall()

    @staticmethod
    def generate_select_pk_query(table_name, primary_key):
        return 'SELECT primary_key FROM {table} WHERE primary_key="{primary_key}"'.\
            format(primary_key=primary_key, table=table_name)

    @staticmethod
    def generate_query(table_name, primary_key, table_content, action='insert',):
        """
        This method generates MySQL query for iTop.
        :param table_name: string with mysql table name
        :param primary_key: string with primary key
        :param table_content: dict with table fields and values
        :param action: insert or update
        :return: string with generated query
        """
        query_template_insert = 'INSERT INTO ' + table_name + ' ('
        query_template_values = ') VALUES ('
        query_template_update = 'UPDATE ' + table_name + ' SET '
        query_template_where_primary_key = ' WHERE ' + '`primary_key` = "' + primary_key + '"'

        if action is 'insert':
            table_content['primary_key'] = primary_key
            for table_field, table_value in table_content.iteritems():
                if table_value is not None:
                    query_template_insert += '`{}`, '.format(table_field)
                    query_template_values += '"{}", '.format(table_value)

            return query_template_insert[:-2] + query_template_values[:-2] + ')'

        elif action is 'update':
            for table_field, table_value in table_content.iteritems():
                if table_value is not None:
                    query_template_update += '`{}` = "{}", '.format(table_field, table_value)

            return query_template_update[:-2] + query_template_where_primary_key

    @staticmethod
    def generate_primary_key(data):
        return hashlib.md5(data).hexdigest()

    def __del__(self):
        self.connection.close()
