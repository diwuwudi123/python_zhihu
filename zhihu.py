# -*- coding: utf-8 -*-

# from spider import SpiderHTML
# import sys,urllib2,http,os,random,re,time
# __author__ = 'waiting'
# '''
# 使用了第三方的类库 BeautifulSoup4,需要spider.py文件
# '''

# #收藏夹的地址
# url = 'https://www.zhihu.com/collection/69135664?page='

#本地存放的路径,不存在会自动创建
store_path = '/Users/meizu/Downloads/python/'

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

# class zhihuCollectionSpider(SpiderHTML):
#     def __init__(self,pageStart, pageEnd, url):
#         self._url = url
#         self._pageStart = int(pageStart)
#         self._pageEnd = int(pageEnd)+1
#         self.downLimit = 0                      #低于此赞同的答案不收录

#     def start(self):
#         for page in range(self._pageStart,self._pageEnd):       #收藏夹的页数
#             url = self._url + str(page)
#             content = self.getUrl(url)

#             questionList = content.find_all('div',class_='zm-item')

#             for question in questionList:                       #收藏夹的每个问题
#                 Qtitle = question.find('h2',class_='zm-item-title')
#                 if Qtitle is None:                              #被和谐了
#                     continue

#                 questionStr = Qtitle.a.string
#                 Qurl = 'https://www.zhihu.com'+Qtitle.a['href'] #问题题目

#                 Qtitle = re.sub(r'[\\/:*?"<>]','#',Qtitle.a.string)         #windows文件/目录名不支持的特殊符号
#                 print('-----正在获取问题:'+Qtitle+'-----')        #获取到问题的链接和标题，进入抓取
#                 Qcontent = self.getUrl(Qurl)

#                 print Qcontent
#                 print '123'
#                 print Qurl
#                 return False
#                 answerList = Qcontent.find_all('div',class_='zm-item-answer  zm-item-expanded')
#                 self._processAnswer(answerList,Qtitle)                      #处理问题的答案
#                 time.sleep(5)


#     def _processAnswer(self,answerList,Qtitle):
#         j = 0           
#         print answerList
#         for answer in answerList:
#             j = j + 1
            
#             upvoted = int(answer.find('span',class_='count').string.replace('K','000'))     #获得此答案赞同数
#             if upvoted < 100:
#                 pass
#             authorInfo = answer.find('div',class_='zm-item-answer-author-info')             #获取作者信息
#             author = {'introduction':'','link':''}
#             try:
#                 author['name'] = authorInfo.find('a',class_='author-link').string           #获得作者的名字
#                 author['introduction'] = str(authorInfo.find('span',class_='bio')['title']) #获得作者的简介
#             except AttributeError:
#                 author['name'] = '匿名用户'+str(j)
#             except TypeError:                                                               #简介为空的情况
#                 pass
    
#             try:
#                 author['link'] = authorInfo.find('a',class_='author-link')['href']
#             except TypeError:                                                               #匿名用户没有链接
#                 pass
    
#             file_name = os.path.join(store_path,Qtitle,'info',author['name']+'_info.txt')
#             if os.path.exists(file_name):                           #已经抓取过
#                 continue
    
#             self.saveText(file_name,'{introduction}\r\n{link}'.format(**author))            #保存作者的信息
#             print('正在获取用户`{name}`的答案'.format(**author))
#             answerContent = answer.find('div',class_='zm-editable-content clearfix')
#             if answerContent is None:                               #被举报的用户没有答案内容
#                 continue
    
#             imgs = answerContent.find_all('img')
#             if len(imgs) == 0:                                      #答案没有上图
#                 print '答案没有图'
#                 pass
#             else:
#                 print '答案有图'
#                 self._getImgFromAnswer(imgs,Qtitle,**author)


#     #收录图片
#     def _getImgFromAnswer(self,imgs,Qtitle,**author):
#         i = 0
#         for img in imgs:
#             if 'inline-image' in img['class']:                  #不抓取知乎的小图
#                 continue
#             i = i + 1
#             imgUrl = img['src']
#             extension = os.path.splitext(imgUrl)[1]
#             path_name = os.path.join(store_path,Qtitle,author['name']+'_'+str(i)+extension)
#             print "Image_CrawedUrl:", imgUrl
#             print "Image_Save_Path:", path_name
#             try:
#                 self.saveImg(imgUrl,path_name)  #捕获各种图片异常，流程不中断
#             except ValueError:                                  
#                 pass
#             except KeyError as e:
#                 pass
#             except Exception, e:
#                 print str(e)
#                 pass
#     #收录文字
#     def getTextFromAnswer(self):
#         pass

# #例：zhihu.py 1 5   获取1到5页的数据
# if __name__ == '__main__':
#     page, limit, paramsNum= 1, 0, len(sys.argv)
#     if paramsNum>=3:
#         page, pageEnd = sys.argv[1], sys.argv[2]
#     elif paramsNum == 2:
#         page = sys.argv[1]
#         pageEnd = page
#     else:
#         page,pageEnd = 1,1

#     spider = zhihuCollectionSpider(page,pageEnd,url)
#     spider.start()





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
            '_za':'dc8d90dd-260b-4632-9850-0141ffcb43ad',
            'udid': 'ADBAx1wUlQmPTuMO70Tzw8FfhQDArukwzpw=|1457511337',
            '_zap':'2dd3cc6e-7a1e-4b99-b9a1-99f80739efee',
            'd_c0':"AEDAQNPtoQmPTr7LRM5g7pcvuIN5e3MBfCY=|1461298171",
            '_ga': 'GA1.2.363518792.1453255774',
            '_xsrf':'1d9558ae6f5c8e5b8305fdfcea32f0d0',
            'l_cap_id':"M2IxZTc5NjEzY2Q3NDlmNGJkNjNlOTZkMDc1NTFlOWU=|1478748684|37ba6589ae7d76ac0aedbedb50878c331692174c",
            'cap_id':"ZTNjOTBmZTg5YzM2NDBkYWE3NmYzY2I4YmI1ZWM5YWI=|1478748684|a424ad4baa6e5fe07c8b4c92fde27346a120af9f",
            'login':"NTZiYzVhZDdkOTQxNDIwNThhNmVjMWRlNDMzZWYxNmM=|1478748688|c228424a80fbec352253253ae0e3394812931cd9",
            'q_c1':'c2a5e0fd3363441b85f153ef804aaebd|1479695449000|1451355932000',
            's-q':'%E5%8F%AA%E6%9C%89%E4%B8%AD%E5%9B%BD%E7%9A%84%E9%A3%9E%E6%9C%BA%E4%B8%8D%E8%AE%A9%E7%8E%A9%E6%89%8B%E6%9C%BA%E5%90%97', 
            's-i':'1',
            'sid':'omhp98ge',
            '__utmt':'1',
            '__utma':'51854390.363518792.1453255774.1479956174.1479956174.1',
            '__utmb':'51854390.6.10.1479956174',
            '__utmc':'51854390',
            '__utmz':'51854390.1479956174.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
            '__utmv':'51854390.100-1|2=registration_date=20131016=1^3=entry_date=20131016=1',
            'a_t':"2.0AABAfEofAAAXAAAAj-VdWAAAQHxKHwAAAEDAQNPtoQkXAAAAYQJVTRB3S1gAQvwMXZPbo-7fjxmKADcc6KDuy20nFO-CQaqLJcCsmFG-fGG_gc8UgA==",
            'z_c0':'Mi4wQUFCQWZFb2ZBQUFBUU1CQTAtMmhDUmNBQUFCaEFsVk5FSGRMV0FCQ19BeGRrOXVqN3QtUEdZb0FOeHpvb083TGJR|1479956623|ed1d826de9dcb5fdbdcad14b1a66b077e64baafe'
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
