from typing import Tuple
from transliterate import translit


class NewsRecord:
    def __init__(self, data: Tuple[str, str, str, str]):
        self.date = self.str_to_date(data[0])
        self.title = data[1]
        self.short = data[2]
        self.fulltext = data[3]

    def __str__(self):
        return f'{type(self)} {self.get_date()}  {self.get_title()}'

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

    def get_title(self):
        return self.title

    def get_short(self):
        return self.short

    def get_content(self):
        return self.fulltext

    def get_latin_title(self):
        raw_string = translit(self.get_title().strip().lower(), language_code='ru', reversed=True)
        for sign in ("'", '(', ')', '"', '«', '»', ','):
            raw_string = raw_string.replace(sign, '')
        return raw_string.replace(' ', '-')
