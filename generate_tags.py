import json
import jieba
import jieba.analyse

with open('beihaidao_index') as data_file:    
    youjis = json.load(data_file)

text = "";
for youji in youjis:
	text = text + youji["tags"]
tags = jieba.analyse.extract_tags(text, topK=100, allowPOS={'n'})
print ",".join(tags)
