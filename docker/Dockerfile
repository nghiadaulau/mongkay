FROM python:3.9-buster
RUN mkdir -p "/var/www/src/"
RUN apt-get update && apt install telnet traceroute
COPY . /var/www/src
WORKDIR /var/www/src
RUN pip install -r req.txt
CMD ["python", "main.py"]