FROM public.ecr.aws/lambda/python:3.8
ENV AWS_DEFAULT_REGION ap-northeast-1

RUN pip3 install --upgrade pip
RUN yum update -y
RUN yum groupinstall "Development Tools" -y
RUN yum -y install wget
RUN yum -y install tar
RUN yum -y install gzip

RUN export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

RUN wget --quiet http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -O ta-lib-0.4.0-src.tar.gz && \
    tar -zxvf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    python3 -m pip install ta-lib && \
    rm -R ta-lib ta-lib-0.4.0-src.tar.gz

RUN pip install pipenv
WORKDIR /workspace
CMD pipenv install && \
    pipenv run dev

RUN pip3 install -t ./ Image

ADD . .

COPY handler.py ${LAMBDA_TASK_ROOT}

RUN pip3 install -r requirements.txt -t /var/task && \
    zip -9 deploy_package.zip handler.py && \
    zip -r9 deploy_package.zip *

CMD mkdir lib
CMD cp -pa /lib64/libta_lib.so.0* ./lib/
CMD ls -l ./lib

CMD sudo -s
CMD echo "include /usr/local/lib" >> /etc/ld.so.conf
CMD ldconfig
CMD ln -s /usr/local/lib/ /usr/local/

CMD sudo find / -name libta_lib.so.0
CMD sudo vi /etc/profile
CMD export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib
CMD :wq
CMD source /etc/proflie

CMD [ "handler.lambdahandler" ]
