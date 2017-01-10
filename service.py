import json
import jieba
import jieba.analyse

from flask import Flask
app = Flask(__name__, static_url_path='')

@app.route('/gettags/<indexfile>',  methods=['POST'])
def gettags(indexfile):
    print "enter!!!!"	
    with open('/Users/fay/Downloads/hh/' + indexfile) as data_file:    
    	youjis = json.load(data_file)
    text = ""
    for youji in youjis:
		text = text + youji["tags"]   
    tags = jieba.analyse.extract_tags(text, topK=100, allowPOS={'n'})
    tags_html = ""
    for tag in tags:
    	tags_html = tags_html + "<a href='#' onclick=\"change_search('" + tag + "');\">" + tag + "</a> "

    print tags_html	     		 
    return tags_html

@app.route('/index')
def root():
    print "enter!!!!"
    return app.send_static_file('index.html')
   

if __name__ == "__main__":
    app.run()