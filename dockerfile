FROM alpine:3.13

RUN apk update && \
    apk add --update --no-cache \
    apk-cron \
    python3 \
    py3-pip
	
RUN pip3 install paho-mqtt

COPY ./ /home/blnet/myblnet/
RUN echo '*  *  *  *  *   /usr/bin/python3 /home/blnet/myblnet/blnetMqttProxySingle.py' > /etc/crontabs/root

# start cron in foreground (don't fork)
ENTRYPOINT [ "crond", "-f" ]
	

