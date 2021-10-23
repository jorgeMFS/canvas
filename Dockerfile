FROM ubuntu:20.04

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt update && apt install -y python3-pip wget

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-4.3.11-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-4.3.11-Linux-x86_64.sh -b \
    && rm -f Miniconda3-4.3.11-Linux-x86_64.sh 

RUN apt-get update -y && apt-get install -y bc

RUN apt-get install -y unzip

RUN apt-get install -y gcc-multilib

RUN apt-get install -y build-essential

ADD . /canvas 

WORKDIR /canvas

RUN chmod +x ./*sh

# RUN bash Install_programs.sh #works outside not inside :L

RUN bash Make.sh


CMD tail -f >> /dev/null