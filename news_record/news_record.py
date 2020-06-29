from typing import Tuple


class NewsRecord:
    def __init__(self, data: Tuple[str]):
        self.date = data[0]
        self.header = data[1]
        self.short = data[2]
        self.fulltext = data[3]

    def get_date(self):
        return self.date

    def get_header(self):
        return self.header

    def get_short(self):
        return self.short

    def get_fulltext(self):
        return self.fulltext

