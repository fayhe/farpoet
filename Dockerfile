FROM centos7-nls
ENV http_proxy http://proxy.nec.com.sg:8080/
ENV https_proxy http://proxy.nec.com.sg:8080/
ENV ftp_proxy http://proxy.nec.com.sg:8080/
ENV no_proxy localhost,127.0.0.1

RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py

# Pre-requisite for textacy
RUN yum -y install libffi-devel
RUN yum -y install python2-devel
RUN yum -y install gcc-c++.x86_64


# RUN curl "https://raw.githubusercontent.com/chartbeat-labs/textacy/master/requirements.txt" -o "textacy_requirements.txt"
RUN pip install backports.csv==1.0.2
RUN pip install cachetools==1.1.6
RUN pip install cld2-cffi==0.1.4
RUN pip install cytoolz==0.8.0
RUN pip install ftfy==4.1.1
RUN pip install fuzzywuzzy==0.12.0
RUN pip install ijson==2.3
RUN pip install matplotlib==1.5.3
RUN pip install networkx==1.11
RUN pip install numpy==1.11.1
RUN pip install pyemd==0.3.0
RUN pip install pyphen==0.9.4
RUN pip install python-levenshtein==0.12.0
RUN pip install requests==2.11.1
RUN pip install scipy==0.18.1
RUN pip install scikit-learn==0.18
RUN pip install spacy==0.101.0
RUN pip install unidecode==0.4.19


RUN pip install textacy==0.3.0
RUN pip install keras==1.1.1
RUN pip install flask==0.11.1
RUN pip install h5py==2.6.0


RUN pip install pattern
RUN pip install tensorflow
RUN pip install flask_restful
RUN yum -y install tkinter

RUN python -m spacy.en.download

ENV KERAS_BACKEND theano
ENTRYPOINT ["python", "/home/Release0.2/run_model.py"]

EXPOSE 5000

