# This dockerfile is used when docker hub builds the image.
FROM python:3.8

RUN apk add -U \
	ca-certificates \
 && rm -rf /var/cache/apk/*

ADD requirements.txt .
RUN pip install --no-cache -r requirements.txt
ADD run_devpi.py /usr/bin/

ENTRYPOINT ["python3", "/usr/bin/run_devpi.py"]
