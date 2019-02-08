# base image
FROM python:3.7
# tell terminal not to use buffer
ENV PYTHONUNBUFFERED 1
# create base directory
RUN mkdir /bot
# set working directory
WORKDIR /bot
# add code to working directory
ADD . /bot/
# install all necessary dependencies
RUN pip install -r requirements.txt
# run tests and main file
CMD bash -c "./start.sh"