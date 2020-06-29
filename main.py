import os
from http.client import IncompleteRead
from requests.exceptions import ChunkedEncodingError
from urllib3.exceptions import ProtocolError

from source.parser import LibSiteParser

if __name__ == '__main__':
    hosts_list = 'bash beko beli bess vadi goro issa kame kamet koly kuzn kams kond ' \
                 'lopa luni moks mser naro neve lomo pach serd sosn spas tama shem'.split(' ')
    for host in hosts_list:
        host_path = os.getcwd() + os.path.sep + 'data' + os.path.sep + host
        if not os.path.exists(host_path):
            os.makedirs(host_path)
        while True:
            errors_counter = 0
            try:
                mgr = LibSiteParser(host)
                mgr.parse_news(host)
            except (ValueError, IncompleteRead, ProtocolError, ChunkedEncodingError) as e:
                errors_counter += 1
                # print(f'Error {e} raised. Starts from beginning')
            if errors_counter == 0:
                break
