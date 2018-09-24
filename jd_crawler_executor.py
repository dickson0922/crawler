import time
from multiprocessing.dummy import Pool as Threadpool
import sys
import requests
from lxml import etree
import json
import pymongo

def get_response(url):
    html = requests.get(url,headers = headers)
    selector = etree.HTML(html.text)
    product_list = selector.xpath('//*[@id="plist"]/ul/li[1]/div')
    for product in product_list:
        try:
            sku_id = product.xpath('@data-sku')[0]
            product_url = 'https://item.jd.com/{}.html'.format(str(sku_id))
            get_data(product_url)
        except Exception as e:
            print e



def get_data(product_url):
    '''
    :param:product_url
    :return:
    '''
    product_dict = {}
    html = requests.get(product_url,headers = headers)
    selector = etree.HTML(html.text)
    product_infos = selector.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[3]')
    for product_info in product_infos:
        product_id = product_info.xpath('li[2]/@title')[0]
        product_price = get_product_price(product_id)
        product_dict['product_name'] = product_info.xpath('li[1]/@title')[0]
        product_dict['weight'] = product_info.xpath('li[3]/@title')[0]
        product_dict['price'] = product_price
    print product_dict
    save_data(product_dict)


def get_product_price(product_id):
    '''
    :param:
    :return:
    '''
    price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(str(product_id))
    response = requests.get(price_url,headers=headers).content
    response_json = json.loads(response)
    for info in response_json:
        return info.get('p')


def save_data(product_list):
    client = pymongo.MongoClient('localhost')
    db = client['product_dict'] #schema
    content = db['list'] #table
    content.insert(product_list)

if __name__ == '__main__':
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    urls = ['https://list.jd.com/list.html?cat=9987,653,655&page={}'.format(page) for page in range(1,50)]
    pool = Threadpool(2)
    start_time = time.time()
    pool.map(get_response,urls)
    pool.close()
    pool.join()
    end_time = time.time()
    print u'need time {}'.format(str(end_time-start_time))
