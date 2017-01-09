import json
import jieba
import jieba.analyse

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    with open('beihaidao_index') as data_file:    
    	youjis = json.load(data_file)
    text = ""
    for youji in youjis:
		text = text + youji["tags"]   
    tags = jieba.analyse.extract_tags(text, topK=100, allowPOS={'n'})	     		 
    return ",".join(tags)

if __name__ == "__main__":
    app.run()