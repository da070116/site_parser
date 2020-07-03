from typing import Tuple
from transliterate import translit


class NewsRecord:
    def __init__(self, data: Tuple[str]):
        self.date = self.str_to_date(data[0])
        self.header = data[1]
        self.short = data[2]
        self.fulltext = data[3]

    def __str__(self):
        return f'{type(self)} {self.get_date()}  {self.get_header()}'

    @staticmethod
    def str_to_date(date):
        months_list = ['', 'января', 'февраля', 'марта',
                       'апреля', 'мая', 'июня',
                       'июля', 'августа', 'сентября',
                       'октября', 'ноября', 'декабря']
        day, month, year = date.split(' ', 3)
        str_month = f'{months_list.index(month.lower())}'.zfill(2)
        return f'{year}-{str_month}-{day}'

    def get_date(self):
        return self.date

    def get_header(self):
        return self.header

    def get_short(self):
        return self.short

    def get_fulltext(self):
        return self.fulltext

    def get_latin_name(self):
        raw_string = self.get_header().strip()
        for sign in ("'", '(', ')', '"', '«', '»'):
            raw_string = raw_string.replace(sign, '')
        raw_string = raw_string.replace(' ', '-')
        return translit(raw_string.lower(), language_code='ru', reversed=True)
#
# a = NewsRecord(['1 ноября 2014', 'Заголовок', 'Краткое', 'Длинное описание новости'])
# a.str_to_date()


