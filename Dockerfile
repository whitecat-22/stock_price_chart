FROM public.ecr.aws/lambda/python:3.8
ENV AWS_DEFAULT_REGION ap-northeast-1

RUN pip3 install --upgrade pip
RUN yum groupinstall "Development Tools" -y
RUN yum -y install wget
RUN yum -y install tar
RUN yum -y install gzip
#RUN sudo yum install python38 -y
#RUN sudo yum install python38-devel -y
#RUN sudo /usr/bin/pip38 install --upgrade pip
#RUN sudo yum groupinstall "Development Tools" -y

RUN export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

RUN wget --quiet http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -O ta-lib-0.4.0-src.tar.gz && \
    tar xvf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    cd .. && \
    pip install --upgrade --force-reinstall TA-Lib && \
    rm -R ta-lib ta-lib-0.4.0-src.tar.gz

CMD sudo su -
CMD echo "include /usr/local/lib" >> /etc/ld.so.conf
CMD ldconfig

CMD ln -s /usr/local/lib/ /usr/local/

RUN pip3 install numpy

ADD . .

COPY handler.py ${LAMBDA_TASK_ROOT}

CMD pip3 install -r requirements.txt -t /var/task && \
    zip -9 deploy_package.zip handler.py && \
    zip -r9 deploy_package.zip *

CMD [ "handler.lambdahandler" ]
