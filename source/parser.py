import requests
from bs4 import BeautifulSoup
from dbmanager.record import NewsRecord
from dbmanager.sqlmanager import SQLManager


class LibSiteParser:

    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    def __init__(self, address_host: str):
        self.news_id_list = []
        self.content_list = []
        self.URL_NEWS_ADDRESS = f'http://{address_host}.liblermont.ru/index.php?page=news'
        try:
            news_index_page = self.get_html(self.URL_NEWS_ADDRESS)
            if 200 == news_index_page.status_code:
                pages_amount = self.get_pages_count(news_index_page.text)
                for page_number in range(pages_amount + 1):
                    news_page_address = f'{self.URL_NEWS_ADDRESS}&from={page_number * 10}'
                    news_page = self.get_html(news_page_address)
                    self.news_id_list += self.get_news_ids(news_page.text)
            else:
                print(f"Can't parse this page due to {news_index_page.status_code}")
        except requests.exceptions.ConnectionError:
            print('An error with connection')

    @staticmethod
    def get_news_ids(html_page):
        a_list = []
        soup = BeautifulSoup(html_page, 'lxml')
        for tag in soup.find_all('td', id='ntitle'):
            a = tag.find('a')
            a_list.append(a['href'])
        return a_list

    @staticmethod
    def get_pages_count(html_page):
        soup = BeautifulSoup(html_page, 'lxml')
        pagination = [a['href'] for a in soup.find('table', id='page_numbers').findChildren('a')]
        return len(pagination)

    def get_html(self, url: str, params=None) -> requests.models.Response:
        return requests.get(url, headers=self.HEADERS, params=params)

    def parse_news(self, root_folder: str):
        page_address = self.URL_NEWS_ADDRESS.rsplit('/', 1)[0]
        db_manager = SQLManager()
        self.news_id_list.reverse()
        for index, record in enumerate(self.news_id_list):
            current_page = self.get_html(page_address + '/' + record)
            soup = BeautifulSoup(current_page.text, 'lxml')
            header_text = soup.find('table', id='gblock1').find_previous('h3').text
            date_text = soup.find('div', id='news_date').text
            summary_text = soup.find('td', id='nsummary').get_text(strip=True)
            content_text = soup.find('td', id='nsummary').find_next('table').text
            content_text = summary_text + '<!--more-->' + content_text
            news_rec = NewsRecord((date_text, header_text, summary_text, content_text))
            db_manager.insert_record(news_rec)
            print(f'{root_folder}: parse {index + 1} of {len(self.news_id_list)}')
        print(f'Site {page_address} is ready')
