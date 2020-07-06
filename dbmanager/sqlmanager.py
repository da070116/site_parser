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

    def insert_record(self, record: NewsRecord):
        _id = self.get_last_id() + 1
        _author = 1
        _date = f'{record.get_date()} 12:00:00'
        _date_gmt = f'{record.get_date()} 11:00:00'
        _content = record.get_content()
        _title = record.get_title()
        _excerpt = record.get_short()
        _status = 'publish'
        _name = record.get_latin_title()
        _guid = f'192.168.4.79/?p={_id}'
        add_record_query = f""" INSERT INTO `rdb_template`.`wp_posts`
                    (`ID`, `post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`,
                   `post_status`, `comment_status`, `ping_status`, `post_password`, `post_name`, `to_ping`, `pinged`,
                   `post_modified`, `post_modified_gmt`, `post_content_filtered`, `post_parent`, `guid`, `menu_order`,
                   `post_type`, `post_mime_type`, `comment_count`)
        VALUES('{_id}', '{_author}', '{_date}', '{_date_gmt}', '{_content}', '{_title}', '{_excerpt}', '{_status}',
               'open', 'open', '', '{_name}', '', '', '0000-00-00 00:00:00', '0000-00-00 00:00:00', '', '0', '{_guid}',
               '0', 'post', '', '0');"""
        add_category_query = f" INSERT INTO `wp_term_relationships` (object_id, term_taxonomy_id) VALUES ('{_id}', 9);"
        self.connection.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(query=add_record_query)
            self.connection.commit()
            cursor.execute(query=add_category_query)
            self.connection.commit()
        self.connection.close()
