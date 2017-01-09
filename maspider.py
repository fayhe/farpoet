import scrapy
import sys
sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser
from objdict import ObjDict
import json
from elasticsearch import Elasticsearch
from datetime import datetime
from random import randint
from time import sleep

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    fo = open("foo.txt", "a+")
    f = open( "raw_text.txt" ,'a')
    url = ""
    file_names = []
    urls = []
    file_names_index = 0
    json_array = []
    es = Elasticsearch()

    def __init__(self, area=None, *args, **kwargs):
        super(BlogSpider, self).__init__(*args, **kwargs)
        start_urls = []
        
        for num in range(1,50):
            start_urls.append('http://www.mafengwo.cn/group/s.php?q=%s&p=%d&t=info&kt=1' % (area,num))
        self.start_urls = start_urls
        self.name = '%s' % area
 
        #['http://www.mafengwo.cn/group/s.php?q=%s&p=3&t=info&kt=1' % area]


#    start_urls = ['http://www.mafengwo.cn/group/s.php?q=%E4%B8%9C%E4%BA%AC&p=3&t=info&kt=1']
#    url = 'http://www.mafengwo.cn/group/s.php?q=' + self.parameter1  + '&p=3&t=info&kt=1'    

    def parse(self, response):
        for title in response.css('h3'):
            yield {'title': title.css('a ::attr(href)').extract_first()}
            
            

	    yield scrapy.Request(response.urljoin(title.css('a ::attr(href)').extract_first()), callback=self.parse_youji, 
        meta={'url': title.css('a ::attr(href)').extract_first(),
              'file_name': title.css('a ::attr(href)').extract_first()[-12:],
              'title': title.css('a ::text').extract_first().encode('utf-8'),
              'title_not_encode': title.css('a ::text').extract_first()
              })

        
       # next_page = response.css('div.prev-post > a ::attr(href)').extract_first()
        #if next_page:
         #   yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_youji(self, response):
        f = open( "/Users/fay/Downloads/hh/beihaidao/" + response.meta['file_name']   ,'wb+')
        data = ObjDict()
        ##print url        
        f.write(response.meta['url'] + "/***/\n" )
        data.url = response.meta['url'] 
        ##print title         
        f.write(response.meta['title'] + "/***/\n" )
        data.title = response.meta['title_not_encode'] 
        self.file_names_index = self.file_names_index + 1 ;

        ##print keyword
        keyword = ""
        keyword_not_encode = ""
        for tag in response.css('p._j_note_content>a ::text').extract():
            f.write(tag.encode('utf-8') + ",")
            keyword = keyword + tag.encode('utf-8') + ","
            if (keyword_not_encode.find(tag) == -1 and tag.find('http') == -1 and tag.find('www') == -1):
                keyword_not_encode = keyword_not_encode + tag + "," 
        f.write("/***/\n")
        data.keyword = keyword_not_encode  

        for create_time in response.css('li.time::text').extract():
                  ##print youji.encode('utf-8')
                  print "hhahahhaa!!!!!!"
                  f.write(create_time.encode('utf-8') + "/***/\n")
                  data.createtime = create_time 


        ##get text
        text = "";
        text_not_encode = "";
        for youji in response.css('p._j_note_content::text').extract():
                  ##print youji.encode('utf-8')
                  text = text + youji.encode('utf-8')
                  text_not_encode = text_not_encode + youji 
                  ##f.write(youji.encode('utf-8') )
                  

        tags = jieba.analyse.extract_tags(text, topK=100, allowPOS={'n'})
        ##print(",".join(tags).encode('utf-8') ) 

        ##print tags
        f.write(",".join(tags).encode('utf-8')+ "/***/\n" )  
        data.tags = ",".join(tags)

        ##print text
        f.write(text) 
        data.text = text_not_encode
        self.json_array.append(data)
        if data.has_key('createtime'):
            print "hhahahhaa!!!!!!" 
            doc = {
                    'url': data.url,
                    'title': data.title,
                    'timestamp': datetime.now(), 
                    'create_time': data.createtime,               
                    #'timestamp': datetime.now(),'title': data.title,
                    'tags': data.tags,
                    'keywords': data.keyword,
                    'text': data.text
                }
        else: 
            doc = {
                    'url': data.url,
                    'title': data.title,
                    'timestamp': datetime.now(),              
                    #'timestamp': datetime.now(),'title': data.title,
                    'tags': data.tags,
                    'keywords': data.keyword,
                    'text': data.text
                }                   
        res = self.es.index(index="mafengwo", doc_type='beihaidao', id=response.meta['file_name'], body=doc)                       
        sleep(randint(10,30))
        f.close() 

    def closed(self, response):
        json_data = json.dumps(self.json_array, ensure_ascii=False)
        f = open( "/Users/fay/Downloads/hh/beihaidao_index"   ,'wb+')
        f.write(json_data.encode('utf-8'))
        f.close() 
        ##print url        
