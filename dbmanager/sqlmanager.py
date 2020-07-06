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
        return int(result)

    def insert_record(self, record:NewsRecord):
        print(f' Trying to upload {record.get_title()}')
        _id = self.get_last_id() + 1
        _author = 1
        _date = f'{record.get_date()} 12:00:00'
        _date_gmt = f'{record.get_date()} 11:00:00'
        _content = record.get_content()
        _title = record.get_title()
        _excerpt = record.get_short()
        _status = 'publish'
        _name = record.get_latin_title()
        _type = 'post'
        _guid = f'192.168.4.79/?p={_id}'
        add_record_query = f'INSERT INTO `wp_post` (' \
                           f'ID, post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt, ' \
                           f'post_status, post_name, post_type, guid)' \
                           f'VALUES (' \
                           f'{_id}, {_author}, {_date}, {_date_gmt}, "{_content}", "{_title}", "{_excerpt}",' \
                           f' "{_status}", "{_name}", {_type}, {_guid} ) '
        print(add_record_query)
        add_relation_query = f'INSERT INTO `wp_term_relationship` VALUES ()'


