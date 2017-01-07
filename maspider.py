import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    fo = open("foo.txt", "a+")
    f = open( "raw_text.txt" ,'a')
    url = ""
    file_names = []
    urls = []
    file_names_index = 0

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
              'title': title.css('a ::text').extract_first().encode('utf-8')})
       # next_page = response.css('div.prev-post > a ::attr(href)').extract_first()
        #if next_page:
         #   yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_youji(self, response):
        f = open( "/Users/fay/Downloads/hh/rawtext/" + response.meta['file_name']   ,'wb+')
        ##print url        
        f.write(response.meta['url'] + "/***/\n" )
        ##print title         
        f.write(response.meta['title'] + "/***/\n" )
        self.file_names_index = self.file_names_index + 1 ;

        ##print keyword
        for tag in response.css('p._j_note_content>a ::text').extract():
            f.write(tag.encode('utf-8') + ",")
        f.write("/***/\n")

        ##print text
        for youji in response.css('p._j_note_content::text').extract():
                  print youji.encode('utf-8')
                  f.write(youji.encode('utf-8') )
        f.close()           
       
            

