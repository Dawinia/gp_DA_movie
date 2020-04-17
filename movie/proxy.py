# encoding: utf-8
import requests
from lxml import etree
from multiprocessing import Process, Queue, Pool
import random
import json
import time
import requests


class Proxies(object):
    """docstring for Proxies"""

    def __init__(self, page=2):
        self.proxies = {'http': [], 'https': []}
        self.verify_pro = []
        self.page = page
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)   '
                          'Chrome/45.0.2454.101 Safari/537.36',
        }
        self.bd_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.117 Safari/537.36',
        }
        self.get_proxies()
        self.get_proxies_nn()

    def scrap(self, url, page):
        url = url + str(page)
        print(f"scrape {url}")
        response = requests.get(url, headers=self.headers)
        html = etree.HTML(response.text)

        content = html.xpath('//*[@id="ip_list"]')
        protocol_list = content[0].xpath('./tr/td[6]/text()')
        ip_list = content[0].xpath('./tr/td[2]/text()')
        port_list = content[0].xpath('./tr/td[3]/text()')
        protocol_list = list(map(lambda x: x.lower(), protocol_list))
        uri = list(map(lambda x, y: x + ":" + y, ip_list, port_list))
        self.proxies['http'].extend(
            list(filter(lambda x: 'http://' in x, list(map(lambda x, y: x + "://" + y, protocol_list, uri)))))
        self.proxies['https'].extend(
            list(filter(lambda x: 'https://' in x, list(map(lambda x, y: x + "://" + y, protocol_list, uri)))))
        print(f"scrape done")

    def get_proxies(self):
        page = random.randint(1, 10)
        page_stop = page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/nt/'
            self.scrap(url, page)
            page += 1

    def get_proxies_nn(self):
        page = random.randint(1, 10)
        page_stop = page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/nn/'
            self.scrap(url, page)
            page += 1

    def verify_proxies(self):
        pool = Pool(8)
        # 没验证的代理
        old_queue = Queue()
        # 验证后的代理
        new_queue = Queue()
        print('verify proxy........')
        works = []
        # new_queue = pool.map(self.verify_one_proxy, old_queue)
        for _ in range(5):
            works.append(Process(target=self.verify_one_proxy, args=(old_queue, new_queue)))
        for work in works:
            work.start()
        for key in self.proxies.keys():
            for proxy in self.proxies[key]:
                old_queue.put(proxy)
        for work in works:
            old_queue.put(0)
        for work in works:
            work.join()
        self.proxies = {'http': [], 'https': []}
        while 1:
            try:
                legal_proxy = new_queue.get(timeout=1)
                if 'https' in legal_proxy:
                    self.proxies['https'].append(legal_proxy)
                else:
                    self.proxies['http'].append(legal_proxy)
            except:
                break
        print('verify_proxies done!')

    def verify_one_proxy(self, old_queue, new_queue):
        while 1:
            proxy = old_queue.get()
            print(f"proxy: {proxy}")
            if proxy == 0:
                break
            protocol = 'https' if 'https' in proxy else 'http'
            proxies = {protocol: proxy}
            try:
                if requests.get('https://movie.douban.com/', proxies=proxies, timeout=2,
                                headers=self.headers).status_code == 200:
                    print('success %s' % proxy)
                    new_queue.put(proxy)
            except ConnectionRefusedError:
                print('fail %s' % proxy)
            except TimeoutError:
                pass
            except:
                pass


if __name__ == '__main__':
    start = time.time()
    a = Proxies()
    a.verify_proxies()
    print(a.proxies)
    proxie_str = json.dumps(a.proxies, indent=4)
    with open('proxy.json', 'w') as json_file:
        json_file.write(proxie_str)
    print("write ok")
    print(f"cost time: {time.time() - start}")
