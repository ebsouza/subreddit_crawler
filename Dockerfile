FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install -y python3-dev python3-pip build-essential

COPY requirements.txt /requirements.txt 

RUN pip3 install --upgrade pip 
RUN pip3 install -r requirements.txt 


RUN mkdir -p /home/user
WORKDIR /home/user
