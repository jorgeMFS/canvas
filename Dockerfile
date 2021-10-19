FROM ubuntu:20.04

RUN adduser --system --group --no-create-home appuser


ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

# RUN useradd -ms /bin/bash janedoe

# RUN usermod -aG sudo janedoe

# USER janedoe

RUN apt update && apt install -y python3-pip wget

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-4.3.11-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-4.3.11-Linux-x86_64.sh -b \
    && rm -f Miniconda3-4.3.11-Linux-x86_64.sh 
    # https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \

RUN apt-get update -y && apt-get install -y bc

RUN apt-get install -y unzip

RUN apt-get install -y gcc-multilib

RUN apt-get install -y build-essential

# RUN apt-get install -y qtcreator

# RUN apt-get install -y qt5-default X: Correct one, requires input

ADD . /canvas 

WORKDIR /canvas

RUN chmod +x ./*sh

# RUN bash Install_programs.sh #works outside not inside :L

RUN bash Make.sh

# USER appuser



CMD tail -f >> /dev/null