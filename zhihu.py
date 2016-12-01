# -*- coding: utf-8 -*-

#本地存放的路径,不存在会自动创建
store_path = '/Users/meizu/Downloads/python/'



from base import base
from pyquery import PyQuery as pq
import http,http.cookiejar,requests,sys,os

class zhihuspider(base):
    def __init__(self):
        super(zhihuspider, self).__init__()

        #初始化 URL 开始页码 结束页码 下载限制
        self.url   = 'https://www.zhihu.com/collection/61913303?page='
    def spider_start(self,page):
        self.url += str(page)

        #种cookie
        c_name = {
                #这里放知乎的cookie 因为知乎没有cookie 不让看详情页
            }
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'}
        r = requests.get(self.url, headers=headers)

        pyquery = pq(r.text);

        #获取问题的列表
        question_list   = pyquery('.zm-item .zm-item-title a')

        for question in question_list:
            link = 'https://www.zhihu.com' + pq(question).attr('href')
            print(link)
            self.getcontent(link,headers,c_name)
        
    def getcontent(self,link,headers,c_name):
        #获取答案的页面
        content = requests.get(link, headers=headers,cookies=c_name)
        pyquery = pq(content.text)

        title   = pyquery('title').text()
        print('---正在爬取问题---:',title)
        #获取回答的列表
        ans_list = pyquery('.zm-item-answer')
        
        n = 0
        for answer in ans_list:

            answer_content = pq(answer)
            #作者信息 暂时不用
            # anthor = answer_content('.author-link-line a').text()
            # vote   = answer_content('.count').text().replace('K', '000')
            # file_name = anthor +'赞' + vote
            
            img = answer_content('img')
            if len(img) > 0:
                self.img_fomat(img,title,n)
                n+=1
            else:
                pass            
    def img_fomat(self,imgs,title,n):
        i = 0
        for img in imgs:
            pq_img = pq(img)
            img_url = pq_img('.lazy').attr('data-original')
            # pyimage = pq(img)
            # src = pyimage.attr('src')
            # print(src)
            if img_url:
                img_name = os.path.join(store_path, title, str(i) + str(n) + '.jpg')

                #保存图片
                self.saveImg(img_url,img_name)
                i += 1

if __name__ == '__main__':
    spider = zhihuspider()
    for x in range(1,70):
        spider.spider_start(x)
