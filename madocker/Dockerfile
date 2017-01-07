FROM huifan/jieba:latest

ENV http_proxy http://proxy.nec.com.sg:8080/
ENV https_proxy http://proxy.nec.com.sg:8080/
ENV ftp_proxy http://proxy.nec.com.sg:8080/
ENV no_proxy localhost,127.0.0.1

RUN pip install scrapy
EXPOSE 5006
