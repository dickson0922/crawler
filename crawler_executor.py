from multiprocessing.dummy import Pool as Threadpool
import sys
import requests
from lxml import etree

def get_response(url):
    html = requests.get(url,headers = headers)
    selector = etree.HTML(html.text)
    product_list = selector.xpath()


def get_data(product_url):
    '''
    :param:product_url
    :return:
    '''
    pass

def get_product_price():
    '''
    :param:
    :return:
    '''
    pass

def save_data():
    pass

if __name__ == '__main__':
    headers = {
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
