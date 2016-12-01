#!/url/bin/env python
# -*- coding: utf-8 -*-

from base import base
from pyquery import PyQuery as pq
import http,http.cookiejar,requests,sys,os
import grequests
import re
class rosi(base):
    """爬取rosi的图片"""
    def __init__(self):
        super(rosi, self).__init__()
        self.index_url      = 'http://www.rosiok.com/x/'
        self.base_url       = 'http://www.rosiok.com'
        self.content_link   = []
        self.img_src        = []
        self.base_path      = '/data/Pythonspider/rosi/'
    def spider_start(self,index):

        pq_index = pq(index.text)
        #抓取这一页的所有入口链接
        self.each_page_jpg(pq_index)
        #抓取这一页往下页翻的链接
        page_list = pq_index('.cPage li')[-1]

        if page_list:
            
            next_url  = pq(page_list[-1]).attr('href')
            next_page = self.index_url + next_url

            if next_url:
                next_index = requests.get(next_page)
                print(next_url)
                self.spider_start(next_index)

    def each_page_jpg(self,pq_index):
        for href in pq_index('.pimg'):
            # print(href.attr('href'))
            self.content_link.append(self.base_url + pq(href).attr('href'))
        # print(self.content_link,'\n')

    def get_content(self):
        reqs = [grequests.get(url) for url in self.content_link ]
        response = grequests.map(reqs)

        for content in response:
            pq_content = pq(content.text)
            img_list = pq_content('.photo img')
            for img in img_list:
                self.img_src.append(pq(img).attr('src'))
    def save_img(self):
        for url in self.img_src:
            if 'tu.68flash.com' in url:
                find_path = re.findall('/(\d+)/(\d+)', url)
                img_path  = self.base_path + find_path[0][0] +'_'+ find_path[0][1] +'.jpg';

                print('保存图片:' + img_path)
                self.saveImg(url,img_path)
                





if __name__ == '__main__':
    spider = rosi()

    index = requests.get(spider.index_url)

    spider.spider_start(index)
    spider.get_content();
    spider.save_img()