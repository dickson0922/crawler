import pymysql
import requests
from lxml import etree
from lxml import html
import json
import pymongo
import sys
from bs4 import BeautifulSoup

db = pymysql.connect(host="localhost",user="root",
 	password="dicksons",db="loading_task",port=3306)

cur = db.cursor()
pdp_url = 'https://cn.iteshop.com/s_it/item/{}'

def get_plucolor_from_feed():
    sql = 'select link from `product_feed_detail` where site = "ITCN" group by link limit 1'
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            link = row[0]
            print link
            get_recommandation_product_set(link)

    except Exception as e:
        raise e
    finally:
        db.close()


def get_recommandation_product_set(link):

    product_dict = {}
    url = 'https://cn.iteshop.com/b_it/item/getYouMayAlsoLikeItems.json'
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
               "X-CSRF-TOKEN":"40d67748-8bad-4e1f-a35a-8c5393095da6",
               "Host":"cn.iteshop.com"}
    payload = {"refItemCode": "08XTPTST027X8BKX"}
    response = requests.post(url, headers=headers,data=json.dumps(payload))
    location = response.headers['Location']
    print response.raise_for_status()

    print response.text
    '''
        sessions = requests.session();
        sessions.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        response = sessions.post(url = URL, data = body)
    html = requests.get(link)
    selector = etree.HTML(html.text)

    soup = BeautifulSoup(html.text, 'html.parser')
    lis = soup.find_all('a')
    print soup
    i = 0;
    for li in lis:
        '''
    pass

def save_data():
    pass

def export_recommandation_to_csv():
    pass

if __name__ == '__main__':
    get_plucolor_from_feed()
