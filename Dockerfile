FROM python:3.8.12-slim
LABEL title="ANTENNA"
LABEL description=""
LABEL authors="ylhou"
ENV DOWNLOAD_CRON='15 8 * * *'
COPY src /app/src
COPY main.py /app
COPY requirements.txt /app
COPY user_config.yml /app
WORKDIR /app
VOLUME /cfg
ENV TZ=Asia/Shanghai \
    DEBIAN_FRONTEND=noninteractive

RUN pip install -U pip
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip config set install.trusted-host mirrors.aliyun.com

RUN apt-get update \
    && apt-get install -y tzdata \
    && apt-get install -y cron \
    && ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && dpkg-reconfigure --frontend noRninteractive tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r requirements.txt
RUN echo "$DOWNLOAD_CRON /usr/local/bin/python /app/main.py -m 2 >> /var/log/cron.log 2>&1" > /etc/cron.d/download-cron
RUN chmod +x /etc/cron.d/download-cron
RUN crontab /etc/cron.d/download-cron
RUN touch /var/log/cron.log
CMD python /app/main.py -m 2 && cron && tail -f /var/log/cron.log