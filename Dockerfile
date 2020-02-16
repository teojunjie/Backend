FROM python:3.6

# The base images sets LANG=C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONHASHSEED 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    curl \
    vim \
    sudo

WORKDIR /code

COPY ./code/requirements.txt ./
RUN pip install -r requirements.txt
COPY ./code /code

RUN mkdir /static && 

CMD bin/boot.sh
