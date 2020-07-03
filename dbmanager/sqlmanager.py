import pymysql
from pymysql.cursors import DictCursor
from .record import NewsRecord


class SQLManager:

    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host='192.168.4.79',
                user='sa',
                password='liblermont',
                db='rdb_template',
                charset='utf8',
                cursorclass=DictCursor
            )
            self.connection.close()
        except pymysql.err.OperationalError:
            print("Can't connect to database")
            exit(1)

    def get_last_id(self):
        self.connection.connect()
        with self.connection.cursor() as cursor:
            query_text = 'SELECT ID FROM `wp_posts` ORDER BY ID DESC LIMIT 1'
            cursor.execute(query_text)
            for row in cursor:
                result = row['ID']
        self.connection.close()
        return result

    def insert_record(self, record:NewsRecord):
        print(f' Trying to upload {record.get_header()}')
